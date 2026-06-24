from src.core.config.bot import BotConfig
from src.infrastructure.di.providers.bot import _normalize_proxy_url


def test_normalize_socks5h_to_socks5():
    assert _normalize_proxy_url("socks5h://host:1080") == "socks5://host:1080"


def test_normalize_socks4a_to_socks4():
    assert _normalize_proxy_url("socks4a://host:1080") == "socks4://host:1080"


def test_normalize_passthrough_for_known_schemes():
    assert _normalize_proxy_url("socks5://host:1080") == "socks5://host:1080"
    assert _normalize_proxy_url("http://host:8080") == "http://host:8080"


def test_botconfig_exposes_custom_api_server_fields():
    assert "api_url" in BotConfig.model_fields
    assert "api_file_url" in BotConfig.model_fields
