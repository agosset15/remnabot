import hashlib
import uuid
from decimal import Decimal
from hmac import compare_digest
from typing import Any, Final
from urllib.parse import urlencode
from uuid import UUID

from aiogram import Bot
from fastapi import Request
from fastapi.responses import PlainTextResponse
from httpx import AsyncClient
from loguru import logger

from src.application.dto import PaymentGatewayDto, PaymentResultDto
from src.application.dto.payment_gateway import RobokassaGatewaySettingsDto
from src.core.config import AppConfig
from src.core.enums import TransactionStatus

from .base import BasePaymentGateway


# https://docs.robokassa.ru/ru/invoice-api/
class RobokassaGateway(BasePaymentGateway):
    _client: AsyncClient

    PAYMENT_URL: Final[str] = "https://auth.robokassa.ru/Merchant/Index.aspx"

    # Name of the Shp_* parameter used to carry our internal UUID.
    SHP_ORDER_ID: Final[str] = "Shp_order_id"

    def __init__(self, gateway: PaymentGatewayDto, bot: Bot, config: AppConfig) -> None:
        super().__init__(gateway, bot, config)

        if not isinstance(self.data.settings, RobokassaGatewaySettingsDto):
            raise TypeError(
                f"Invalid settings type: expected {RobokassaGatewaySettingsDto.__name__}, "
                f"got {type(self.data.settings).__name__}"
            )

        # No API client needed — Robokassa uses redirect-based payments.
        self._client = self._make_client(base_url=self.PAYMENT_URL)

    async def handle_create_payment(self, amount: Decimal, details: str) -> PaymentResultDto:
        order_id = uuid.uuid4()
        # Robokassa requires a numeric InvId; we use 0 (auto-assigned) and carry
        # our UUID in a Shp_ parameter so we can identify it in the webhook.
        inv_id = 0
        out_sum = f"{amount:.2f}"

        signature = self._sign_payment(out_sum, inv_id, str(order_id))
        payment_url = self._build_payment_url(
            out_sum=out_sum,
            inv_id=inv_id,
            description=details,
            signature=signature,
            order_id=str(order_id),
        )

        return PaymentResultDto(id=order_id, url=payment_url)

    async def handle_webhook(self, request: Request) -> tuple[UUID, TransactionStatus]:
        logger.debug(f"Received {self.__class__.__name__} webhook request")

        # Robokassa sends notifications as form-data (POST) or query params (GET).
        form = await request.form()
        webhook_data = dict(form) if form else dict(request.query_params)

        if not self._verify_webhook(webhook_data):
            raise PermissionError("Webhook verification failed")

        order_id_str = webhook_data.get(self.SHP_ORDER_ID)
        if not order_id_str:
            raise ValueError(f"Required field '{self.SHP_ORDER_ID}' is missing")

        payment_id = UUID(order_id_str)

        # Robokassa only calls ResultURL on successful payment — no explicit cancel status.
        return payment_id, TransactionStatus.COMPLETED

    def build_ok_response(self, inv_id: str | int) -> PlainTextResponse:
        return PlainTextResponse(content=f"OK{inv_id}")

    def _sign_payment(self, out_sum: str, inv_id: int, order_id: str) -> str:
        settings = self.data.settings  # type: ignore[union-attr]
        raw = (
            f"{settings.merchant_login}"  # type: ignore[union-attr]
            f":{out_sum}"
            f":{inv_id}"
            f":{settings.password1.get_secret_value()}"  # type: ignore[union-attr]
            f":{self.SHP_ORDER_ID}={order_id}"
        )
        return self._hash(raw, settings.hash_algorithm)  # type: ignore[union-attr, arg-type]

    def _sign_webhook(self, out_sum: str, inv_id: str, order_id: str) -> str:
        """
        Signature for ResultURL verification (Password #2).
        Formula: MD5(OutSum:InvId:Password2:Shp_order_id=<uuid>)
        """
        settings = self.data.settings  # type: ignore[union-attr]
        raw = (
            f"{out_sum}"
            f":{inv_id}"
            f":{settings.password2.get_secret_value()}"  # type: ignore[union-attr]
            f":{self.SHP_ORDER_ID}={order_id}"
        )
        return self._hash(raw, settings.hash_algorithm)  # type: ignore[union-attr,arg-type]

    @staticmethod
    def _hash(raw: str, algorithm: str = "md5") -> str:
        algo = algorithm.lower().replace("-", "")
        h = hashlib.new(algo, raw.encode("utf-8"))
        return h.hexdigest().upper()

    def _build_payment_url(
        self,
        out_sum: str,
        inv_id: int,
        description: str,
        signature: str,
        order_id: str,
    ) -> str:
        settings = self.data.settings  # type: ignore[union-attr]
        params: dict[str, Any] = {
            "MerchantLogin": settings.merchant_login,  # type: ignore[union-attr]
            "OutSum": out_sum,
            "InvId": inv_id,
            "Description": description,
            "SignatureValue": signature,
            self.SHP_ORDER_ID: order_id,
            "Culture": "ru",
        }

        # if settings.is_test:
        #     params["IsTest"] = 1

        return f"{self.PAYMENT_URL}?{urlencode(params)}"

    def _verify_webhook(self, data: dict) -> bool:
        received_sign = data.get("SignatureValue", "").upper()
        out_sum = data.get("OutSum", "")
        inv_id = data.get("InvId", "")
        order_id = data.get(self.SHP_ORDER_ID, "")

        if not received_sign or not out_sum or not inv_id:
            logger.warning("Webhook is missing required fields (OutSum / InvId / SignatureValue)")
            return False

        if not order_id:
            logger.warning(f"Webhook is missing '{self.SHP_ORDER_ID}' field")
            return False

        expected = self._sign_webhook(out_sum, inv_id, order_id)

        if not compare_digest(expected, received_sign):
            logger.warning("Invalid Robokassa webhook signature")
            return False

        return True
