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
from src.application.dto.payment_gateway import PayMasterGatewaySettingsDto
from src.core.config import AppConfig
from src.core.enums import TransactionStatus

from .base import BasePaymentGateway


# https://paymaster.ru/docs/en/api/
class PayMasterGateway(BasePaymentGateway):
    _client: AsyncClient

    API_BASE: Final[str] = "https://paymaster.ru/api/v2"

    def __init__(self, gateway: PaymentGatewayDto, bot: Bot, config: AppConfig) -> None:
        super().__init__(gateway, bot, config)

        if not isinstance(self.data.settings, PayMasterGatewaySettingsDto):
            raise TypeError(
                f"Invalid settings type: expected {PayMasterGatewaySettingsDto.__name__}, "
                f"got {type(self.data.settings).__name__}"
            )

        self._client = self._make_client(
            base_url=self.API_BASE,
            headers={
                "Authorization": f"Bearer {self.data.settings.api_key.get_secret_value()}",  # type: ignore[union-attr]
                "Accept": "application/json",
            },
        )

    async def handle_create_payment(self, amount: Decimal, details: str) -> PaymentResultDto:
        order_id = str(uuid.uuid4())
        payload = await self._create_payment_payload(str(amount), details, order_id)
        headers = {"Idempotency-Key": order_id}

        try:
            response = await self._client.post("invoices", json=payload, headers=headers)
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

        webhook_data = await self._get_webhook_data(request)

        # PayMaster does not provide a webhook signature — use a secret path in callbackUrl
        # (token embedded in the URL) as recommended in the docs.

        invoice: dict = webhook_data.get("invoice", {})
        order_id_str = invoice.get("orderNo")

        if not order_id_str:
            raise ValueError("Required field 'invoice.orderNo' is missing")

        status = webhook_data.get("status")
        payment_id = UUID(order_id_str)

        match status:
            case "Settled" | "Authorized":
                transaction_status = TransactionStatus.COMPLETED
            case "Cancelled" | "Rejected":
                transaction_status = TransactionStatus.CANCELED
            case _:
                raise ValueError(f"Unsupported payment status: {status}")

        return payment_id, transaction_status

    async def _create_payment_payload(
        self, amount: str, details: str, order_id: str
    ) -> dict[str, Any]:
        settings = self.data.settings  # type: ignore[union-attr]
        return {
            "merchantId": settings.merchant_id,  # type: ignore[union-attr]
            "invoice": {
                "description": details,
                "orderNo": order_id,
            },
            "amount": {
                "value": float(amount),
                "currency": str(self.data.currency),
            },
            "protocol": {
                "returnUrl": await self._get_bot_redirect_url(),
                "callbackUrl": self.config.get_webhook(self.data.type),
            },
        }

    def _get_payment_data(self, data: dict[str, Any], order_id: str) -> PaymentResultDto:
        payment_url = data.get("url")
        if not payment_url:
            raise KeyError("Invalid response from PayMaster API: missing 'url'")

        return PaymentResultDto(id=UUID(order_id), url=str(payment_url))
