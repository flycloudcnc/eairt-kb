"""Configuration loaded from environment variables."""
import os


class Settings:
    host: str = os.getenv("EAIRT_KB_HOST", "0.0.0.0")
    port: int = int(os.getenv("EAIRT_KB_PORT", "8000"))
    log_level: str = os.getenv("EAIRT_KB_LOG_LEVEL", "info")
    db_url: str = os.getenv("EAIRT_KB_DB_URL", "sqlite:///./eairt_kb.db")


settings = Settings()
