from pydantic_settings import BaseSettings, SettingsConfigDict

# Application configuration loaded from environment variables and .env.
class Settings(BaseSettings):
    github_api_base_url: str = "https://api.github.com"
    request_timeout: float = 5.0
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
