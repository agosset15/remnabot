from src.application.dto import PaymentGatewayDto
from src.application.dto.payment_gateway import HeleketGatewaySettingsDto
from src.core.config import AppConfig
from src.infrastructure.services.bot_registry import BotRegistry

from .cryptomus import CryptomusGateway


# https://doc.heleket.com/
class HeleketGateway(CryptomusGateway):
    API_BASE: str = "https://api.heleket.com"

    NETWORKS = ["31.133.220.8"]

    def __init__(self, gateway: PaymentGatewayDto, bots: BotRegistry, config: AppConfig) -> None:
        super().__init__(gateway, bots, config)

        if not isinstance(self.data.settings, HeleketGatewaySettingsDto):
            raise TypeError(
                f"Invalid settings type: expected {HeleketGatewaySettingsDto.__name__}, "
                f"got {type(self.data.settings).__name__}"
            )
