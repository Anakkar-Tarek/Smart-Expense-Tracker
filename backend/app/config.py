from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    # Database
    database_url: str = "sqlite:///./expenses.db"

    # File upload
    upload_dir: str = "./uploads"
    max_upload_size: int = 5 * 1024 * 1024

    # Environment
    environment: str = "development"

    # CORS
    cors_origins: list[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ]

    # Logging
    log_level: str = "INFO"

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()

os.makedirs(settings.upload_dir, exist_ok=True)
