"""Configuration management for mcp-server-steam."""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    steam_api_key: str | None = Field(
        default=None,
        description="Steam Web API key from https://steamcommunity.com/dev/apikey"
    )
    steam_user_id: str | None = Field(
        default=None,
        description="Default Steam User ID (64-bit) for API calls"
    )
    steam_api_base_url: str = Field(
        default="https://api.steampowered.com",
        description="Base URL for Steam Web API"
    )
    request_timeout: float = Field(
        default=10.0,
        description="HTTP request timeout in seconds"
    )
    max_retries: int = Field(
        default=3,
        description="Maximum number of retry attempts for failed requests"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
