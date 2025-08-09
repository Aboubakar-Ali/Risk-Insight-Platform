from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # Configuration de la base de données
    DATABASE_URL: str = "postgresql://risk_user:risk_password@localhost:5432/risk_insight"
    
    # Configuration du backend
    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 8000
    DEBUG: bool = True
    
    # APIs externes
    OPENAI_API_KEY: Optional[str] = None
    OPENWEATHER_API_KEY: Optional[str] = None
    
    # Sécurité
    SECRET_KEY: str = "your-secret-key-change-in-production"
    JWT_SECRET: str = "your-jwt-secret-change-in-production"
    
    # Logs
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings() 