"""Application configuration settings."""

from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with environment variable support."""

    # Application
    app_name: str = "SHAERER"
    app_version: str = "1.0.0"
    app_env: str = "development"
    app_debug: bool = False
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    app_workers: int = 4

    # Security
    app_secret_key: str = "your-secret-key-change-in-production"
    jwt_secret_key: str = "your-jwt-secret-key-change-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expiration: int = 3600
    jwt_refresh_expiration: int = 604800

    # Database
    database_url: str = "sqlite:///./shaerer.db"
    database_echo: bool = False
    database_pool_size: int = 20
    database_max_overflow: int = 10

    # CORS
    cors_origins: list = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ]
    cors_allow_credentials: bool = True
    cors_allow_methods: list = ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"]
    cors_allow_headers: list = ["Content-Type", "Authorization"]

    # LLM
    llm_provider: str = "openai"
    llm_model: str = "gpt-4-turbo-preview"
    llm_api_key: str = ""
    llm_temperature: float = 0.7
    llm_max_tokens: int = 2000
    llm_timeout: int = 30

    # Voice
    voice_stt_provider: str = "google"
    voice_stt_api_key: str = ""
    voice_stt_language: str = "en-US"
    voice_tts_provider: str = "google"
    voice_tts_api_key: str = ""
    voice_tts_language: str = "en-US"
    voice_tts_voice: str = "en-US-Neural2-C"
    voice_wake_word: str = "hey shaerer"
    voice_wake_word_sensitivity: float = 0.5
    voice_sample_rate: int = 16000
    voice_channels: int = 1
    voice_chunk_size: int = 1024

    # Image
    image_provider: str = "openai"
    image_api_key: str = ""
    image_model: str = "gpt-4-vision-preview"
    image_max_size: int = 5242880
    image_allowed_formats: str = "jpg,jpeg,png,gif,webp"

    # Files
    file_upload_dir: str = "./uploads"
    file_max_size: int = 52428800
    file_allowed_extensions: str = "txt,pdf,doc,docx,xls,xlsx,csv,json,py,js,html,css"
    file_chunk_size: int = 1048576

    # Memory
    memory_vector_provider: str = "openai"
    memory_vector_model: str = "text-embedding-3-small"
    memory_vector_api_key: str = ""
    memory_max_context: int = 10000
    memory_min_importance: float = 0.3
    memory_retention_days: int = 365

    # Email
    email_provider: str = "gmail"
    email_address: str = ""
    email_password: str = ""
    email_smtp_server: str = "smtp.gmail.com"
    email_smtp_port: int = 587

    # Calendar
    calendar_provider: str = "google"
    calendar_api_key: str = ""

    # Weather & News
    weather_provider: str = "openweathermap"
    weather_api_key: str = ""
    news_provider: str = "newsapi"
    news_api_key: str = ""

    # Logging
    log_level: str = "INFO"
    log_format: str = "json"
    log_file: str = "./logs/shaerer.log"

    # Features
    feature_voice_enabled: bool = True
    feature_code_execution_enabled: bool = True
    feature_browser_automation_enabled: bool = True
    feature_email_enabled: bool = True
    feature_calendar_enabled: bool = True
    feature_plugins_enabled: bool = True
    feature_file_upload_enabled: bool = True
    feature_image_analysis_enabled: bool = True

    # API
    api_v1_prefix: str = "/api/v1"
    api_base_url: str = "http://localhost:8000"

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
