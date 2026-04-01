from pydantic import SecretStr

from .base import BaseConfig


class SmtpConfig(BaseConfig, env_prefix="SMTP_"):
    host: str = "localhost"
    port: int = 587
    username: str = ""
    password: SecretStr = SecretStr("")
    sender: str = ""
    use_tls: bool = True
    use_ssl: bool = False
    timeout: int = 10
