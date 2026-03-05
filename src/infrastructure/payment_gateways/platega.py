import hashlib
import hmac
import uuid
from decimal import Decimal
from typing import Any, Final
from uuid import UUID

import orjson
from aiogram import Bot
from fastapi import Request
from httpx import AsyncClient, HTTPStatusError
from loguru import logger

from src.application.dto import PaymentGatewayDto, PaymentResultDto
from src.application.dto.payment_gateway import PlategaGatewaySettingsDto
from src.core.config import AppConfig
from src.core.enums import TransactionStatus

from .base import BasePaymentGateway


# https://docs.platega.io/
class PlategaGateway(BasePaymentGateway):
    _client: AsyncClient

    API_BASE: Final[str] = "https://app.platega.io"

    # Platega does not publish a fixed IP allowlist.
    NETWORKS = []

    def __init__(self, gateway: PaymentGatewayDto, bot: Bot, config: AppConfig) -> None:
        super().__init__(gateway, bot, config)

        if not isinstance(self.data.settings, PlategaGatewaySettingsDto):
            raise TypeError(
                f"Invalid settings type: expected {PlategaGatewaySettingsDto.__name__}, "
                f"got {type(self.data.settings).__name__}"
            )

        self._client = self._make_client(
            base_url=self.API_BASE,
            headers={
                "X-MerchantId": self.data.settings.merchant_id,  # type: ignore[union-attr, dict-item]
                "X-Secret": self.data.settings.api_key.get_secret_value(),  # type: ignore[union-attr]
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
        )

    async def handle_create_payment(self, amount: Decimal, details: str) -> PaymentResultDto:
        order_id = uuid.uuid4()
        payload = await self._create_payment_payload(amount, details, order_id)

        try:
            response = await self._client.post("transactions", json=payload)
            response.raise_for_status()
            data = orjson.loads(response.content)
            return self._get_payment_data(data, order_id)

        except HTTPStatusError as e:
            logger.error(
                f"HTTP error creating payment. "
                f"Status: '{e.response.status_code}', Body: {e.response.text}"
            )
            raise
        except (KeyError, orjson.JSONDecodeError) as e:
            logger.error(f"Failed to parse response. Error: {e}")
            raise
        except Exception as e:
            logger.exception(f"An unexpected error occurred while creating payment: {e}")
            raise

    async def handle_webhook(self, request: Request) -> tuple[UUID, TransactionStatus]:
        logger.debug(f"Received {self.__class__.__name__} webhook request")

        raw_body = await request.body()
        webhook_data = orjson.loads(raw_body)

        if not self._verify_webhook(request, raw_body, webhook_data):
            raise PermissionError("Webhook verification failed")

        transaction: dict = webhook_data.get("transaction", {})
        order_id_str = transaction.get("id")

        if not order_id_str:
            raise ValueError("Required field 'transaction.id' is missing")

        status = webhook_data.get("status") or transaction.get("status")
        payment_id = UUID(order_id_str)

        match status:
            case "success" | "paid" | "completed":
                transaction_status = TransactionStatus.COMPLETED
            case "cancel" | "cancelled" | "failed" | "expired":
                transaction_status = TransactionStatus.CANCELED
            case _:
                raise ValueError(f"Unsupported payment status: {status}")

        return payment_id, transaction_status

    async def _create_payment_payload(
        self, amount: Decimal, details: str, order_id: UUID
    ) -> dict[str, Any]:
        settings = self.data.settings  # type: ignore[union-attr]
        return {
            "id": str(order_id),
            "paymentMethod": settings.payment_method,  # type: ignore[union-attr]
            "paymentDetails": {
                "amount": float(amount),
                "currency": str(self.data.currency),
            },
            "description": details,
            "returnUrl": await self._get_bot_redirect_url(),
            "failedUrl": await self._get_bot_redirect_url(),
            "callbackUrl": self.config.get_webhook(self.data.type),
        }

    def _get_payment_data(self, data: dict[str, Any], order_id: UUID) -> PaymentResultDto:
        # Response fields: redirect (payment URL), transactionId
        payment_url = data.get("redirect")
        if not payment_url:
            raise KeyError("Invalid response from Platega API: missing 'redirect'")

        return PaymentResultDto(id=order_id, url=str(payment_url))

    def _verify_webhook(self, request: Request, raw_body: bytes, data: dict) -> bool:
        received_signature = data.get("signature")
        if not received_signature:
            logger.warning("Webhook is missing 'signature' field")
            return False

        secret = self.data.settings.api_key.get_secret_value().encode()  # type: ignore[union-attr]

        # Build the body for verification: the payload without the 'signature' field
        # (as is standard — sign the payload fields, not the signature itself)
        body_without_sign = {k: v for k, v in data.items() if k != "signature"}
        body_to_verify = orjson.dumps(body_without_sign, option=orjson.OPT_SORT_KEYS)

        expected = hmac.new(secret, body_to_verify, hashlib.sha256).hexdigest()

        if not hmac.compare_digest(expected, received_signature):
            logger.warning("Invalid Platega webhook signature")
            return False

        return True
