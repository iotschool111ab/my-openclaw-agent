"""配置管理模块"""
import os
from typing import Optional
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


class Config:
    """应用配置类"""
    
    # 应用配置
    ENV = os.getenv('ENV', 'development')
    DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    PORT = int(os.getenv('PORT', 5000))
    
    # 平台配置
    PLATFORM = os.getenv('PLATFORM', 'line')
    PLATFORM_TOKEN = os.getenv('PLATFORM_TOKEN')
    PLATFORM_SECRET = os.getenv('PLATFORM_SECRET')
    
    # AI 配置
    AI_PROVIDER = os.getenv('AI_PROVIDER', 'groq')
    AI_MODEL = os.getenv('AI_MODEL', 'llama-3.1-8b-instant')
    AI_API_KEY = os.getenv('AI_API_KEY')
    AI_TIMEOUT = int(os.getenv('AI_TIMEOUT', 30))
    
    # 可选配置
    DATABASE_URL = os.getenv('DATABASE_URL')
    REDIS_URL = os.getenv('REDIS_URL')
    
    @staticmethod
    def validate():
        """验证必要的配置"""
        if not Config.PLATFORM_TOKEN:
            raise ValueError('Missing PLATFORM_TOKEN')
        if not Config.AI_API_KEY:
            raise ValueError('Missing AI_API_KEY')
        return True


# 创建全局配置实例
config = Config()
