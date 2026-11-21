from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # GitHub REST API base URL
    github_api_base_url: str = "https://api.github.com"

    # Timeout for GitHub API requests
    request_timeout: float = 5.0

    # Application logging level
    log_level: str = "INFO"

    # Load configuration from the root-level .env file
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


# Create a settings object that can be imported by other modules
settings = Settings()
