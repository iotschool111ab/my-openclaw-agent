"""最小化 AI Bot 应用模板

这是一个可复用的最小化模板，支持多个聊天平台。
"""

import os
import logging
from dotenv import load_dotenv
from flask import Flask, request
from config import config
from utils.logger import setup_logger
from utils.api import AIAPIClient

# 加载环境变量
load_dotenv()

# 初始化 Flask 应用
app = Flask(__name__)

# 设置日志
logger = setup_logger('ai-agent', config.LOG_LEVEL)

# 初始化 AI 客户端
try:
    ai_client = AIAPIClient(
        provider=config.AI_PROVIDER,
        model=config.AI_MODEL,
        api_key=config.AI_API_KEY,
        timeout=config.AI_TIMEOUT
    )
except Exception as e:
    logger.error(f"Failed to initialize AI client: {e}")
    ai_client = None


def call_ai(message: str, **kwargs) -> str:
    """调用 AI API 获取回复
    
    Args:
        message: 用户消息
        **kwargs: 其他参数
    
    Returns:
        AI 生成的回复
    """
    if not ai_client:
        return "AI 服务不可用"
    
    response = ai_client.call(message, **kwargs)
    return response or "处理失败，请重试"


@app.route('/health', methods=['GET'])
def health():
    """健康检查端点"""
    return {
        'status': 'ok',
        'platform': config.PLATFORM,
        'ai_provider': config.AI_PROVIDER
    }, 200


@app.route('/webhook', methods=['POST'])
def webhook():
    """处理来自聊天平台的 Webhook
    
    支持的平台:
    - LINE: POST /webhook
    - Telegram: POST /webhook
    - Discord: POST /webhook
    - Slack: POST /webhook
    """
    try:
        # 这里添加您的平台特定的处理逻辑
        data = request.get_json()
        logger.info(f"Received webhook: {data}")
        
        if not data:
            return {'error': 'No data'}, 400
        
        # 根据平台处理消息
        if config.PLATFORM == 'line':
            # LINE 平台处理
            events = data.get('events', [])
            for event in events:
                logger.debug(f"LINE event: {event}")
        
        elif config.PLATFORM == 'telegram':
            # Telegram 平台处理
            message = data.get('message', {})
            text = message.get('text')
            logger.debug(f"Telegram message: {text}")
        
        elif config.PLATFORM == 'discord':
            # Discord 平台处理
            content = data.get('content')
            logger.debug(f"Discord message: {content}")
        
        elif config.PLATFORM == 'slack':
            # Slack 平台处理
            event = data.get('event', {})
            text = event.get('text')
            logger.debug(f"Slack message: {text}")
        
        return {'status': 'ok'}, 200
    
    except Exception as e:
        logger.error(f"Webhook error: {e}", exc_info=True)
        return {'error': str(e)}, 500


@app.route('/test', methods=['POST'])
def test():
    """测试端点 - 用于测试 AI 功能"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        
        if not message:
            return {'error': 'No message'}, 400
        
        response = call_ai(message)
        
        return {
            'message': message,
            'response': response,
            'platform': config.PLATFORM,
            'ai_provider': config.AI_PROVIDER
        }, 200
    
    except Exception as e:
        logger.error(f"Test error: {e}", exc_info=True)
        return {'error': str(e)}, 500


@app.errorhandler(404)
def not_found(error):
    """处理 404 错误"""
    return {'error': 'Not found'}, 404


@app.errorhandler(500)
def internal_error(error):
    """处理 500 错误"""
    logger.error(f"Internal error: {error}", exc_info=True)
    return {'error': 'Internal server error'}, 500


if __name__ == '__main__':
    logger.info(f"Starting AI Agent...")
    logger.info(f"  Platform: {config.PLATFORM}")
    logger.info(f"  AI Provider: {config.AI_PROVIDER}")
    logger.info(f"  Debug: {config.DEBUG}")
    logger.info(f"  Port: {config.PORT}")
    
    app.run(
        host='0.0.0.0',
        port=config.PORT,
        debug=config.DEBUG
    )
