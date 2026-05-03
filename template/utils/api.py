"""AI API 调用模块"""
import requests
from typing import Optional
from utils.logger import logger


class AIAPIClient:
    """AI API 客户端"""
    
    def __init__(self, provider: str, model: str, api_key: str, timeout: int = 30):
        """初始化客户端
        
        Args:
            provider: AI 提供商 (groq/openai/anthropic)
            model: 模型名称
            api_key: API 密钥
            timeout: 请求超时时间（秒）
        """
        self.provider = provider
        self.model = model
        self.api_key = api_key
        self.timeout = timeout
    
    def call(self, message: str, **kwargs) -> Optional[str]:
        """调用 AI API
        
        Args:
            message: 用户消息
            **kwargs: 其他参数（温度、最大令牌等）
        
        Returns:
            AI 生成的回复，如果失败返回 None
        """
        if self.provider == 'groq':
            return self._call_groq(message, **kwargs)
        elif self.provider == 'openai':
            return self._call_openai(message, **kwargs)
        elif self.provider == 'anthropic':
            return self._call_anthropic(message, **kwargs)
        else:
            logger.error(f'Unsupported provider: {self.provider}')
            return None
    
    def _call_groq(self, message: str, **kwargs) -> Optional[str]:
        """调用 Groq API"""
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            data = {
                'model': self.model,
                'messages': [{'role': 'user', 'content': message}],
                'max_tokens': kwargs.get('max_tokens', 500),
                'temperature': kwargs.get('temperature', 0.7)
            }
            
            response = requests.post(
                'https://api.groq.com/openai/v1/chat/completions',
                headers=headers,
                json=data,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            return response.json()['choices'][0]['message']['content']
        except requests.exceptions.RequestException as e:
            logger.error(f'Groq API error: {e}')
            return None
    
    def _call_openai(self, message: str, **kwargs) -> Optional[str]:
        """调用 OpenAI API"""
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            data = {
                'model': self.model,
                'messages': [{'role': 'user', 'content': message}],
                'max_tokens': kwargs.get('max_tokens', 500),
                'temperature': kwargs.get('temperature', 0.7)
            }
            
            response = requests.post(
                'https://api.openai.com/v1/chat/completions',
                headers=headers,
                json=data,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            return response.json()['choices'][0]['message']['content']
        except requests.exceptions.RequestException as e:
            logger.error(f'OpenAI API error: {e}')
            return None
    
    def _call_anthropic(self, message: str, **kwargs) -> Optional[str]:
        """调用 Anthropic API"""
        try:
            headers = {
                'x-api-key': self.api_key,
                'Content-Type': 'application/json'
            }
            data = {
                'model': self.model,
                'max_tokens': kwargs.get('max_tokens', 500),
                'messages': [{'role': 'user', 'content': message}]
            }
            
            response = requests.post(
                'https://api.anthropic.com/v1/messages',
                headers=headers,
                json=data,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            return response.json()['content'][0]['text']
        except requests.exceptions.RequestException as e:
            logger.error(f'Anthropic API error: {e}')
            return None
