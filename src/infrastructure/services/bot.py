from typing import Optional, Union
from urllib.parse import quote

from aiogram.utils.chat_member import ChatMemberUnion

from src.application.services import WebService
from src.core.config import AppConfig
from src.core.constants import T_ME
from src.core.enums import Deeplink

from .bot_registry import BotRegistry


class BotService:
    """Bot info and links for the bot handling the current update (primary elsewhere)."""

    def __init__(self, bots: BotRegistry, config: AppConfig, web_service: WebService):
        self.bots = bots
        self.config = config
        self.web_service = web_service

    async def _get_bot_redirect_url(self) -> str:
        return await self.bots.url()

    async def is_inline_enabled(self) -> bool:
        me = await self.bots.current.get_me()
        return me.supports_inline_queries or False

    async def get_bot_states(self) -> dict[str, str]:
        bot_info = await self.bots.current.get_me()

        status_map: dict[Optional[bool], str] = {
            True: "Enabled",
            False: "Disabled",
            None: "Unknown",
        }

        return {
            "groups_mode": status_map[bot_info.can_join_groups],
            "privacy_mode": status_map[not bot_info.can_read_all_group_messages],
            "inline_mode": status_map[bot_info.supports_inline_queries],
        }

    async def get_my_name(self) -> str:
        result = await self.bots.current.get_my_name()
        return result.name

    async def get_referral_url(self, referral_code: str) -> str:
        if self.config.web.referral_via_domain:
            web_url = self.web_service.referral(referral_code)
            if web_url:
                return web_url

        base_url = await self._get_bot_redirect_url()
        return Deeplink.REFERRAL.build_url(base_url, referral_code)

    async def get_plan_url(self, public_code: str) -> str:
        base_url = await self._get_bot_redirect_url()
        return Deeplink.PLAN.build_url(base_url, public_code)

    async def get_ad_link_url(self, code: str) -> str:
        base_url = await self._get_bot_redirect_url()
        return Deeplink.ADVERTISING.build_url(base_url, code)

    def get_support_url(self, text: Optional[str] = None) -> str:
        base_url = f"{T_ME}{self.config.bot.support_username.get_secret_value()}"
        encoded_text = quote(text or "")
        return f"{base_url}?text={encoded_text}"

    async def get_chat_member(self, chat_id: Union[str, int], user_id: int) -> ChatMemberUnion:
        return await self.bots.current.get_chat_member(chat_id=chat_id, user_id=user_id)
