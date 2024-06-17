from pydantic import SecretStr
from pydantic_settings import BaseSettings


class TelegramConfig(BaseSettings):
    """Represents the Telegram bot configuration."""

    class Config:
        env_prefix = "TELEGRAM_"

    token: SecretStr
    local_server_url: str = "http://localhost:8081"


class LoggingConfig(BaseSettings):
    """Represents the logging configuration."""

    class Config:
        env_prefix = "LOGGING_"

    level: str = "INFO"
    format: str = "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
    datefmt: str = "%Y-%m-%d %H:%M:%S"
