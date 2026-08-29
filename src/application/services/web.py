from typing import Optional

from src.core.config import AppConfig
from src.core.enums import FaqSection, WebPage


class WebService:
    def __init__(self, config: AppConfig) -> None:
        self._web = config.web

    @property
    def _base_url(self) -> Optional[str]:
        return self._web.base_url

    @property
    def home(self) -> Optional[str]:
        if not self._base_url:
            return None
        return WebPage.HOME.build_url(self._base_url)

    @property
    def plans(self) -> Optional[str]:
        if not self._base_url:
            return None
        return WebPage.PLANS.build_url(self._base_url)

    @property
    def download(self) -> Optional[str]:
        if not self._base_url:
            return None
        return WebPage.DOWNLOAD.build_url(self._base_url)

    @property
    def help(self) -> Optional[str]:
        if not self._base_url:
            return None
        return WebPage.HELP.build_url(self._base_url)

    @property
    def terms(self) -> Optional[str]:
        if not self._base_url:
            return None
        return WebPage.TERMS.build_url(self._base_url)

    @property
    def privacy(self) -> Optional[str]:
        if not self._base_url:
            return None
        return WebPage.PRIVACY.build_url(self._base_url)

    @property
    def success(self) -> Optional[str]:
        if not self._base_url:
            return None
        return WebPage.SUCCESS.build_url(self._base_url)

    def faq(self, section: Optional[FaqSection] = None) -> Optional[str]:
        if not self._base_url:
            return None
        url = WebPage.FAQ.build_url(self._base_url)
        if section:
            return f"{url}#{section}"
        return url

    def purchase(self, plan_id: Optional[str] = None) -> Optional[str]:
        if not self._base_url:
            return None
        if plan_id:
            return WebPage.PURCHASE.build_url(self._base_url, planId=plan_id)
        return WebPage.PURCHASE.build_url(self._base_url)

    def referral(self, referral_code: str) -> Optional[str]:
        if not self._base_url:
            return None
        return WebPage.REFERRAL.build_url(self._base_url, referral_code)
