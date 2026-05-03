# AI Agent 模板快速开始

## 🚀 30 秒快速创建

```bash
# 进入 template 目录
cd template

# 运行生成脚本
bash setup_agent.sh my-awesome-bot line

# 进入项目
cd my-awesome-bot

# 配置凭证
nano .env

# 安装依赖
pip install -r requirements.txt

# 验证设置
python check_setup.py

# 启动应用
python main.py
```

## 📋 支持的聊天平台

### LINE
```bash
bash setup_agent.sh my-line-bot line
```
**需要：** Channel Access Token + Channel Secret

### Telegram
```bash
bash setup_agent.sh my-telegram-bot telegram
```
**需要：** Bot Token

### Discord
```bash
bash setup_agent.sh my-discord-bot discord
```
**需要：** Bot Token

### Slack
```bash
bash setup_agent.sh my-slack-bot slack
```
**需要：** Bot Token + Signing Secret

### 文本 CLI
```bash
bash setup_agent.sh my-cli-bot text
```
**需要：** 无（仅 AI API Key）

## 🔑 获取 API 金钥

### Groq（推荐，免费）
1. 访问 https://console.groq.com/
2. 点击 **Keys** → **Create API Key**
3. 复制您的 API Key

### OpenAI
1. 访问 https://platform.openai.com/api-keys
2. 点击 **Create new secret key**
3. 复制您的 API Key

### Anthropic
1. 访问 https://console.anthropic.com/
2. 获取您的 API Key

## 📁 生成的文件结构

```
my-awesome-bot/
├── main.py                 # 主应用程序
├── config.py              # 配置管理
├── check_setup.py         # 设置检查脚本
├── run.sh                 # 运行脚本
├── .env                   # 环境变量（不要提交）
├── .env.example          # 环境变量示例
├── .gitignore            # Git 忽略规则
├── requirements.txt      # 依赖清单
├── README.md             # 项目文档
├── handlers/             # 消息处理器
│   └── __init__.py
├── utils/                # 工具模块
│   ├── __init__.py
│   ├── logger.py        # 日志配置
│   └── api.py           # API 客户端
└── logs/                 # 日志目录
    └── ai-agent.log
```

## ⚙️ 环境变量配置

### 必需变量

```env
# 平台选择
PLATFORM=line                      # 选择: line/telegram/discord/slack/text

# AI 提供商
AI_PROVIDER=groq                   # 选择: groq/openai/anthropic
AI_MODEL=llama-3.1-8b-instant     # 模型名称
AI_API_KEY=your_api_key_here       # API 金钥

# 平台凭证（根据平台选择）
PLATFORM_TOKEN=your_token_here
PLATFORM_SECRET=your_secret_here   # LINE 需要
```

### 可选变量

```env
# 应用配置
DEBUG=false                # 调试模式
LOG_LEVEL=INFO            # 日志级别
PORT=5000                 # 应用端口
ENV=development           # 环境

# 其他
AI_TIMEOUT=30            # API 超时时间
DATABASE_URL=            # 数据库连接
REDIS_URL=               # Redis 连接
```

## 🧪 验证和测试

### 检查配置
```bash
python check_setup.py
```

### 测试 AI API
```bash
python -c "
from utils.api import AIAPIClient
import os
from dotenv import load_dotenv

load_dotenv()
client = AIAPIClient(
    provider=os.getenv('AI_PROVIDER'),
    model=os.getenv('AI_MODEL'),
    api_key=os.getenv('AI_API_KEY')
)
response = client.call('Hello!')
print(f'Response: {response}')
"
```

### 测试 Flask 应用
```bash
curl http://localhost:5000/health
```

## 🔧 自定义应用

### 添加新的消息处理器

**创建 handlers/text_handler.py：**
```python
def handle_text_message(message: str) -> str:
    """处理文本消息"""
    from utils.api import AIAPIClient
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    client = AIAPIClient(
        provider=os.getenv('AI_PROVIDER'),
        model=os.getenv('AI_MODEL'),
        api_key=os.getenv('AI_API_KEY')
    )
    return client.call(message)
```

### 新增数据库支持

1. 在 `.env` 中设置 `DATABASE_URL`
2. 安装数据库驱动：`pip install sqlalchemy`
3. 创建数据模型
4. 在应用中使用

## 📈 部署

### 使用 Docker

```dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "-b", "0.0.0.0:5000", "main:app"]
```

### 使用 Gunicorn

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 main:app
```

### 环境变量分离

创建 `config/.env.production`：
```env
ENV=production
DEBUG=false
LOG_LEVEL=WARNING
```

运行时加载：
```bash
export ENV_FILE=config/.env.production
python main.py
```

## 🐛 常见问题

**Q: 如何添加更多平台？**
A: 编辑 `setup_agent.sh`，在平台选择部分添加新平台。

**Q: 如何使用多个 AI 提供商？**
A: 编辑 `utils/api.py`，添加对应的 API 调用方法。

**Q: 如何实现对话历史？**
A: 添加数据库支持，存储 `(user_id, message, response)` 组合。

**Q: 如何添加认证？**
A: 在 `main.py` 中添加 Flask-Login 或 JWT 认证。

## 📚 进阶用法

### 使用 Redis 缓存

```python
from redis import Redis

redis_client = Redis.from_url(os.getenv('REDIS_URL'))

def get_cached_response(key):
    return redis_client.get(key)
```

### 实现速率限制

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)
```

### 添加错误追踪

```python
import sentry_sdk

sentry_sdk.init(os.getenv('SENTRY_DSN'))
```

## 📞 获取帮助

- 查看生成项目中的 `README.md`
- 检查 `logs/ai-agent.log` 中的错误信息
- 访问平台官方文档
- 查看原始项目的 `建置指导书.md`

---

**准备好了吗？** 运行 `bash setup_agent.sh my-bot line` 开始! 🚀
