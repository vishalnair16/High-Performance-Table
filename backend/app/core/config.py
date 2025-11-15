from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # MongoDB Settings
    # Option 1: Include database name in URI: mongodb+srv://user:pass@cluster.mongodb.net/database_name?appName=Cluster0
    # Option 2: Use DB_NAME separately (database name will be appended automatically)
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb+srv://username:password@cluster0.84iovxr.mongodb.net/?appName=Cluster0")
    DB_NAME: str = os.getenv("DB_NAME", "high_performance_db")
    
    # Redis Settings
    REDIS_HOST: str = os.getenv("REDIS_HOST", "redis")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_PASSWORD: Optional[str] = os.getenv("REDIS_PASSWORD", None)
    REDIS_DB: int = int(os.getenv("REDIS_DB", "0"))
    
    # Cache Settings
    CACHE_TTL: int = int(os.getenv("CACHE_TTL", "300"))  # 5 minutes default
    
    # API Settings
    API_V1_PREFIX: str = "/api/v1"
    PAGE_SIZE_DEFAULT: int = 50
    PAGE_SIZE_MAX: int = 1000
    
    # Performance Settings
    ENABLE_CACHE: bool = os.getenv("ENABLE_CACHE", "true").lower() == "true"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

