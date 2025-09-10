"""
Application Settings

Configuration settings for the PyStockAuto application.
"""

import os
from typing import Optional
from pydantic import BaseSettings

class Settings(BaseSettings):
    """Application settings"""
    
    # Application settings
    APP_NAME: str = "PyStockAuto"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    HOST: str = "localhost"
    PORT: int = 8000
    
    # Database settings
    DATABASE_URL: str = "mysql+pymysql://user:password@localhost:3306/stockauto"
    DATABASE_ECHO: bool = False
    
    # Korea Investment API settings
    KI_APP_KEY: Optional[str] = None
    KI_APP_SECRET: Optional[str] = None
    KI_BASE_URL: str = "https://openapi.koreainvestment.com:9443"
    
    # Redis settings (for caching and background tasks)
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Logging settings
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Security settings
    SECRET_KEY: str = "your-secret-key-here"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Trading settings
    DEFAULT_ORDER_TIMEOUT: int = 30  # seconds
    MAX_ORDERS_PER_MINUTE: int = 10
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Create global settings instance
settings = Settings()
