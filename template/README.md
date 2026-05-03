# AI Agent 模板 - 快速生成指南

本目录包含可复用的 AI Agent 模板，支持快速创建新的聊天机器人项目。

## 📁 模板结构

```
template/
├── setup_agent.sh           # 快速生成脚本
├── python_apps/            # Python 应用模板
│   ├── minimal_bot.py      # 最小化模板
│   ├── advanced_bot.py     # 高级功能模板
│   └── config.py           # 配置管理模板
├── configs/                # 配置文件模板
│   ├── .env.example        # 环境变量示例
│   ├── requirements.txt    # 依赖文件
│   └── config.yaml         # 配置文件
└── docs/
    ├── README_TEMPLATE.md  # 项目 README 模板
    └── QUICK_START.md      # 快速开始模板
```

## 🚀 快速使用

### 方式 1：使用生成脚本（推荐）

```bash
# 创建新的 AI Agent 项目
bash setup_agent.sh my-new-agent telegram

# 参数说明
# 参数1: 项目名称
# 参数2: 聊天平台 (line/telegram/discord/slack)
```

### 方式 2：手动复制模板

```bash
# 复制整个模板目录
cp -r template/python_apps/minimal_bot.py ./my-agent/main.py
cp template/configs/.env.example ./my-agent/.env
cp template/configs/requirements.txt ./my-agent/
```

## 📋 模板文件说明

### 1. setup_agent.sh
自动化脚本，一键生成新项目：
- 创建项目目录结构
- 复制配置文件
- 初始化 Git（可选）
- 显示下一步指导

### 2. minimal_bot.py
最小化应用模板，包含：
- 基础 Flask 服务器
- 单一聊天平台集成（可切换）
- Groq API 调用
- 错误处理

### 3. advanced_bot.py
高级功能模板，包含：
- 多平台支持
- 数据库集成
- 日志系统
- 插件架构

### 4. config.py
配置管理模板：
- 环境变量加载
- 多环境支持（dev/prod）
- 配置验证
- 安全凭证管理

## 🔧 配置参数

### 支持的聊天平台

| 平台 | 标识 | 需要的凭证 |
|------|------|----------|
| LINE | line | Token + Secret |
| Telegram | telegram | Bot Token |
| Discord | discord | Bot Token |
| Slack | slack | Bot Token |
| 文本 CLI | text | 无 |

### 环境变量模板

所有项目都支持以下基础环境变量：

```env
# AI Provider (可选择: groq/openai/anthropic)
AI_PROVIDER=groq
AI_MODEL=llama-3.1-8b-instant
AI_API_KEY=your_api_key

# Chatbot Platform
PLATFORM=line
PLATFORM_TOKEN=your_token
PLATFORM_SECRET=your_secret

# 应用配置
DEBUG=false
LOG_LEVEL=INFO
PORT=5000
```

## 📝 创建新项目的完整步骤

### 1. 使用脚本创建
```bash
bash template/setup_agent.sh my-awesome-bot line
cd my-awesome-bot
```

### 2. 配置凭证
```bash
# 编辑 .env 文件
nano .env

# 填入您的 API 金钥和平台凭证
```

### 3. 安装依赖
```bash
pip install -r requirements.txt
```

### 4. 验证设置
```bash
python check_setup.py
```

### 5. 启动应用
```bash
python main.py
# 或使用提供的脚本
./run.sh
```

## 🎯 常见使用场景

### 场景 1：创建 Telegram BOT

```bash
bash template/setup_agent.sh telegram-news-bot telegram
cd telegram-news-bot
# 编辑 .env，填入 Telegram Bot Token
python main.py
```

### 场景 2：创建 Discord 机器人

```bash
bash template/setup_agent.sh discord-assistant discord
cd discord-assistant
# 编辑 .env，填入 Discord Bot Token
python main.py
```

### 场景 3：创建多平台支持的 BOT

```bash
bash template/setup_agent.sh multi-platform-bot advanced
cd multi-platform-bot
# 编辑 .env，配置多个平台凭证
python main.py
```

## 📦 文件清单

### 自动生成的项目包含：

```
my-agent/
├── main.py                    # 主应用
├── config.py                  # 配置管理
├── handlers/                  # 消息处理器
│   ├── __init__.py
│   ├── text_handler.py
│   └── media_handler.py
├── utils/                     # 工具函数
│   ├── __init__.py
│   ├── api.py                # API 调用
│   └── logger.py             # 日志配置
├── .env                       # 环境变量
├── .env.example              # 环境变量示例
├── .gitignore                # Git 忽略规则
├── requirements.txt          # 依赖清单
├── run.sh                    # 运行脚本
├── check_setup.py            # 设置检查
├── README.md                 # 项目文档
└── Dockerfile               # Docker 配置（可选）
```

## 🔄 模板更新流程

1. **改进现有项目**
   - 在您的项目中测试新功能
   - 验证功能正常

2. **同步到模板**
   - 将改进的代码复制回 `template/` 目录
   - 更新版本号和变更日志

3. **分享改进**
   - 提交到版本控制
   - 其他项目可以使用最新模板

## 💡 最佳实践

### 1. 环境变量管理
```python
# ✅ 推荐
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('AI_API_KEY')

# ❌ 不推荐
api_key = "hardcoded_key"  # 不要在代码中硬编码
```

### 2. 错误处理
```python
# ✅ 推荐
try:
    response = call_ai_api(message)
except RateLimitError:
    return "API 限制，请稍后重试"
except Exception as e:
    logger.error(f"Error: {e}")
    return "发生错误，请稍后重试"

# ❌ 不推荐
response = call_ai_api(message)  # 无错误处理
```

### 3. 日志记录
```python
# ✅ 推荐
logger.info(f"User {user_id} sent: {message}")
logger.error(f"API call failed: {error}")

# ❌ 不推荐
print("Something happened")  # 无法跟踪或过滤
```

### 4. 配置管理
```python
# ✅ 推荐 - 使用配置类
class Config:
    DEBUG = os.getenv('DEBUG', False)
    PLATFORM = os.getenv('PLATFORM', 'line')
    
config = Config()

# ❌ 不推荐 - 散布在代码中
debug = os.getenv('DEBUG')
platform = os.getenv('PLATFORM')
```

## 📊 模板版本控制

### 当前版本：1.0.0

```
v1.0.0 (2026-05-03)
✅ 基础 LINE, Telegram, Discord 支持
✅ Groq API 集成
✅ 环境变量管理
✅ 错误处理和日志
✅ 快速生成脚本

v1.1.0 (计划)
⬜ 数据库支持
⬜ 对话历史
⬜ 插件系统
```

## 🤝 贡献指南

如果您改进了模板：

1. 测试新功能在实际项目中工作
2. 更新 `template/` 中的相应文件
3. 更新文档
4. 更新版本号
5. 记录变更在 CHANGELOG.md

## 📚 相关资源

- [原始项目](../README.md)
- [建置指导书](../建置指导书.md)
- 各平台 API 文档：
  - [LINE Bot SDK](https://github.com/line/line-bot-sdk-python)
  - [Telegram Bot API](https://core.telegram.org/bots/api)
  - [Discord.py](https://discordpy.readthedocs.io/)
  - [Slack Bolt](https://slack.dev/bolt-python/)

## ❓ 常见问题

**Q: 如何添加新的聊天平台？**
A: 编辑 `setup_agent.sh` 和相应的模板文件，添加新平台的配置。

**Q: 可以同时使用多个平台吗？**
A: 可以，使用 `advanced_bot.py` 模板支持多平台。

**Q: 如何自定义模板？**
A: 直接编辑 `template/` 目录中的文件，或创建您自己的变体。

**Q: 模板多久更新一次？**
A: 与主项目保持同步，有重大改进时更新。

---

**准备好创建您的第一个 AI Agent 了吗？**

```bash
bash template/setup_agent.sh my-first-agent line
```

祝您使用愉快！ 🚀