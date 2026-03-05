import uuid
from base64 import b64decode
from decimal import Decimal
from typing import Any, Final
from uuid import UUID

import orjson
from aiogram import Bot
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from fastapi import Request
from httpx import AsyncClient, HTTPStatusError
from loguru import logger

from src.application.dto import PaymentGatewayDto, PaymentResultDto
from src.application.dto.payment_gateway import WataGatewaySettingsDto
from src.core.config import AppConfig
from src.core.enums import TransactionStatus

from .base import BasePaymentGateway


class WataGateway(BasePaymentGateway):
    _client: AsyncClient

    API_BASE: Final[str] = "https://api.wata.pro/api/h2h"

    # Public key is fetched once and cached for the lifetime of the instance.
    _public_key_pem: bytes | None = None

    def __init__(self, gateway: PaymentGatewayDto, bot: Bot, config: AppConfig) -> None:
        super().__init__(gateway, bot, config)

        if not isinstance(self.data.settings, WataGatewaySettingsDto):
            raise TypeError(
                f"Invalid settings type: expected {WataGatewaySettingsDto.__name__}, "
                f"got {type(self.data.settings).__name__}"
            )

        self._client = self._make_client(
            base_url=self.API_BASE,
            headers={
                "Authorization": f"Bearer {self.data.settings.api_key.get_secret_value()}",  # type: ignore[union-attr]
                "Content-Type": "application/json",
            },
        )

    async def handle_create_payment(self, amount: Decimal, details: str) -> PaymentResultDto:
        order_id = str(uuid.uuid4())
        payload = await self._create_payment_payload(amount, details, order_id)

        try:
            response = await self._client.post("links", json=payload)
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

        if not await self._verify_webhook(request, raw_body):
            raise PermissionError("Webhook verification failed")

        # Skip pre-payment (предоплатный) webhooks — we only act on post-payment.
        kind = webhook_data.get("kind")
        if kind != "Payment":
            raise ValueError(f"Ignoring webhook kind: {kind!r}")

        order_id_str = webhook_data.get("orderId")
        if not order_id_str:
            raise ValueError("Required field 'orderId' is missing")

        status = webhook_data.get("transactionStatus")
        payment_id = UUID(order_id_str)

        match status:
            case "Paid":
                transaction_status = TransactionStatus.COMPLETED
            case "Declined":
                transaction_status = TransactionStatus.CANCELED
            case _:
                raise ValueError(f"Unsupported transactionStatus: {status}")

        return payment_id, transaction_status

    async def _create_payment_payload(
        self, amount: Decimal, details: str, order_id: str
    ) -> dict[str, Any]:
        return {
            "type": "OneTime",
            "amount": float(amount),
            "currency": str(self.data.currency),
            "description": details,
            "orderId": order_id,
            "successRedirectUrl": await self._get_bot_redirect_url(),
            "failRedirectUrl": await self._get_bot_redirect_url(),
        }

    def _get_payment_data(self, data: dict[str, Any], order_id: str) -> PaymentResultDto:
        payment_url = data.get("url")
        if not payment_url:
            raise KeyError("Invalid response from WATA API: missing 'url'")

        return PaymentResultDto(id=UUID(order_id), url=str(payment_url))

    async def _fetch_public_key(self) -> bytes:
        if self._public_key_pem is not None:
            return self._public_key_pem

        try:
            # Use a plain client without auth for the public-key endpoint.
            response = await self._client.get("public-key")
            response.raise_for_status()
            data = orjson.loads(response.content)
            pem_str: str = data["value"]
            self._public_key_pem = pem_str.encode()
            return self._public_key_pem
        except Exception as e:
            logger.error(f"Failed to fetch WATA public key: {e}")
            raise

    async def _verify_webhook(self, request: Request, raw_body: bytes) -> bool:
        signature_b64 = request.headers.get("X-Signature")
        if not signature_b64:
            logger.warning("Webhook is missing 'X-Signature' header")
            return False

        try:
            public_key_pem = await self._fetch_public_key()
            public_key = serialization.load_pem_public_key(public_key_pem)
            signature_bytes = b64decode(signature_b64)

            public_key.verify(
                signature_bytes,
                raw_body,
                padding.PKCS1v15(),
                hashes.SHA512(),
            )
            return True

        except InvalidSignature:
            logger.warning("Invalid WATA webhook RSA signature")
            return False
        except Exception as e:
            logger.error(f"WATA webhook verification error: {e}")
            return False
