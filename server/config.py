import os 
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    """应用配置"""
    # 应用配置
    APP_NAME: str = "创业助手AI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # API配置
    API_V1_PREFIX: str = "/api/v1"
    
    # 大模型配置
    LLM_API_KEY: str = os.getenv("LLM_API_KEY", "")
    LLM_BASE_URL: str = os.getenv("LLM_BASE_URL", "")
    LLM_MODEL_NAME: str = os.getenv("LLM_MODEL", "")


settings = Settings()
