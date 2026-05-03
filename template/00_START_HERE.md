# 📚 下次建置相似 AI Agent 的完整模板

感谢您使用本项目！为了帮助您下次快速建置类似的 AI Agent，我们为您提供了完整的模板系统。

## 🎯 模板系统概览

本模板系统包含所有必要的文件和脚本，让您可以在 **5 分钟内** 创建一个新的 AI Agent 项目。

### 核心特性

✅ **一键生成** - 使用脚本自动创建项目结构  
✅ **多平台支持** - LINE, Telegram, Discord, Slack, Text CLI  
✅ **多 AI 提供商** - Groq, OpenAI, Anthropic  
✅ **即插即用** - 开箱即用的应用框架  
✅ **生产就绪** - 包含日志、配置、错误处理  
✅ **易于定制** - 模块化设计，易于扩展  

---

## 📂 模板文件说明

| 文件 | 说明 | 作用 |
|------|------|------|
| `setup_agent.sh` | 🔴 **必需** | 自动生成新项目 |
| `config.py` | ✅ 推荐 | 配置管理 |
| `requirements.txt` | ✅ 推荐 | 依赖清单 |
| `.env.example` | ✅ 推荐 | 环境变量示例 |
| `python_apps/minimal_bot.py` | ✅ 框架 | Flask 应用模板 |
| `utils/logger.py` | ✅ 工具 | 日志系统 |
| `utils/api.py` | ✅ 工具 | AI API 客户端 |
| `README.md` | 📖 文档 | 模板总体说明 |
| `QUICK_START.md` | 📖 文档 | 快速开始指南 |
| `TEMPLATE_INDEX.md` | 📖 文档 | 模板索引 |

---

## 🚀 使用模板的 3 个步骤

### 第 1 步：生成项目

```bash
cd template
bash setup_agent.sh my-new-agent line
cd my-new-agent
```

**生成的文件：**
```
my-new-agent/
├── main.py                 ✅ 准备好的应用
├── config.py              ✅ 配置管理
├── .env                   ✅ 环境变量
├── requirements.txt       ✅ 依赖列表
├── run.sh                 ✅ 运行脚本
├── check_setup.py         ✅ 验证脚本
└── ...其他文件
```

### 第 2 步：配置凭证

```bash
nano .env
# 填入您的 API 金钥和平台凭证
```

### 第 3 步：启动应用

```bash
pip install -r requirements.txt
python check_setup.py
python main.py
```

**完成！** 🎉

---

## 📋 支持的平台和提供商

### 聊天平台

```bash
# LINE
bash setup_agent.sh my-bot line

# Telegram
bash setup_agent.sh my-bot telegram

# Discord
bash setup_agent.sh my-bot discord

# Slack
bash setup_agent.sh my-bot slack

# 文本 CLI（用于测试）
bash setup_agent.sh my-bot text
```

### AI 提供商

| 提供商 | 成本 | 模型 | 特点 |
|-------|------|------|------|
| **Groq** | 💰 免费 | Llama 3.1 8B | ⚡ 最快 |
| OpenAI | 💵 付费 | GPT-4, 3.5 | 🧠 最强 |
| Anthropic | 💵 付费 | Claude | 🛡️ 最安全 |

---

## 🔑 如何获取凭证

### Groq（推荐）

```
1. 访问 https://console.groq.com/
2. 点击 "Keys" → "Create API Key"
3. 复制生成的密钥
```

### LINE

```
1. 访问 https://developers.line.biz/
2. 创建 Messaging API Channel
3. 复制 Channel Access Token 和 Channel Secret
```

### Telegram

```
1. 联系 @BotFather 在 Telegram 上
2. 创建新 bot
3. 复制生成的 token
```

### Discord

```
1. 访问 https://discord.com/developers/
2. 创建新应用
3. 添加 Bot
4. 复制 Bot Token
```

### Slack

```
1. 访问 https://api.slack.com/apps
2. 创建新应用
3. 生成 Bot Token 和 Signing Secret
```

---

## 📖 文档结构

```
template/
├── README.md              ← 您在这里
├── QUICK_START.md         ← 快速开始
├── TEMPLATE_INDEX.md      ← 详细索引
├── setup_agent.sh         ← 生成脚本
└── 其他文件
```

### 推荐阅读顺序

1. **README.md** (本文件) - 概述和快速指南
2. **QUICK_START.md** - 详细的快速开始步骤
3. **TEMPLATE_INDEX.md** - 所有文件的详细说明

---

## ❓ 常见问题

### Q: 如何添加新的聊天平台？

A: 编辑 `setup_agent.sh`，在 platform case 语句中添加新平台的配置。

### Q: 生成的项目如何定制？

A: 项目完全模块化，请查看 `main.py` 和 `utils/` 目录中的注释了解如何扩展。

### Q: 可以同时使用多个平台吗？

A: 可以，修改 `config.py` 支持多平台配置。

### Q: 如何部署到生产环境？

A: 查看 `Dockerfile.example`，使用 Docker 或 Kubernetes 部署。

### Q: 支持数据库吗？

A: 是的，修改 `config.py` 添加 `DATABASE_URL`，使用 SQLAlchemy。

### Q: 如何实现复杂的对话流？

A: 创建 `handlers/` 模块，实现自定义的消息处理逻辑。

---

## 🛠️ 自定义和扩展

### 项目结构

```
my-agent/
├── main.py                 # 主应用（从模板复制的 minimal_bot.py）
├── config.py              # 配置管理
├── handlers/              # 👈 添加自定义处理器
│   ├── __init__.py
│   ├── text_handler.py   # 文本处理
│   └── media_handler.py  # 媒体处理
├── utils/                # 工具模块
│   ├── logger.py         # 日志
│   ├── api.py            # API 客户端
│   ├── database.py       # 👈 添加数据库模块
│   └── cache.py          # 👈 添加缓存模块
└── models/               # 👈 添加数据模型
    └── message.py
```

### 添加自定义处理器

**handlers/text_handler.py：**
```python
def handle_text_message(message: str) -> str:
    from utils.api import AIAPIClient
    import os
    
    client = AIAPIClient(
        provider=os.getenv('AI_PROVIDER'),
        model=os.getenv('AI_MODEL'),
        api_key=os.getenv('AI_API_KEY')
    )
    return client.call(message)
```

**在 main.py 中使用：**
```python
from handlers.text_handler import handle_text_message

response = handle_text_message(user_message)
```

---

## 🚢 部署选项

### 1. 本地运行

```bash
python main.py
```

### 2. Docker

```bash
docker build -t my-agent .
docker run -p 5000:5000 my-agent
```

### 3. Docker Compose

```bash
docker-compose up -d
```

### 4. 云平台

- **Heroku**：提供 `Procfile` 和 `runtime.txt`
- **AWS**：使用 ECS 或 Elastic Beanstalk
- **Google Cloud**：使用 Cloud Run
- **DigitalOcean**：使用 App Platform

---

## 📊 模板有什么包含？

### 自动生成的功能

✅ 基础 Flask 应用  
✅ 平台特定的 Webhook 处理  
✅ AI API 集成  
✅ 环境变量管理  
✅ 日志系统  
✅ 错误处理  
✅ 健康检查端点  
✅ 测试端点  
✅ 配置验证  
✅ Git 忽略规则  
✅ 依赖管理  

### 无需重新编写的代码

- ✅ HTTP 框架（Flask）
- ✅ API 客户端逻辑
- ✅ 日志配置
- ✅ 配置管理
- ✅ 错误处理
- ✅ Webhook 基础架构

---

## 🎓 学习资源

### 官方文档
- [Flask 文档](https://flask.palletsprojects.com/)
- [LINE Bot SDK](https://github.com/line/line-bot-sdk-python)
- [Groq API](https://console.groq.com/docs)

### 示例项目
- 当前项目：[my-openclaw-agent](../README.md)
- 建置指导书：[建置指导书.md](../建置指导书.md)

### 视频教程
查看平台文档中的官方视频教程

---

## ✨ 提示和最佳实践

### 安全最佳实践

```python
# ✅ 正确 - 使用环境变量
api_key = os.getenv('AI_API_KEY')

# ❌ 错误 - 不要硬编码密钥
api_key = "sk-1234567890abcdef"
```

### 配置管理

```python
# ✅ 正确 - 使用配置类
from config import config
platform = config.PLATFORM

# ❌ 错误 - 散布在代码中
platform = os.getenv('PLATFORM')
```

### 错误处理

```python
# ✅ 正确 - 捕获和记录错误
try:
    response = api_client.call(message)
except APIError as e:
    logger.error(f"API error: {e}")
    return "Error occurred"

# ❌ 错误 - 忽视错误
response = api_client.call(message)
```

### 日志记录

```python
# ✅ 正确 - 使用结构化日志
logger.info(f"User {user_id} message: {message[:50]}")

# ❌ 错误 - 使用 print
print("Something happened")
```

---

## 📝 更新和维护

### 更新模板

当您改进了应用：

1. 更新 `template/` 中的相应文件
2. 更新 `config.py`, `utils/`, 等
3. 测试新更改
4. 更新版本号在 `README.md`
5. 提交到版本控制

### 版本控制

```bash
# 提交改进
git add template/
git commit -m "Improve template: Add X feature"
git push
```

---

## 🤝 贡献

如果您改进了模板或发现了问题：

1. 更新相关文件
2. 测试新变更
3. 更新文档
4. 提交 Pull Request

---

## 📞 获取帮助

1. **查看文档**：`QUICK_START.md` 和 `TEMPLATE_INDEX.md`
2. **检查日志**：`logs/ai-agent.log`
3. **平台支持**：查看各平台官方文档
4. **代码示例**：查看当前项目的 `main_simple.py`

---

## 🎯 下一步

### 立即开始

```bash
cd template
bash setup_agent.sh my-first-agent line
```

### 深入学习

1. 阅读 `QUICK_START.md`
2. 查看生成项目中的注释代码
3. 尝试修改和扩展

### 进阶功能

- 添加数据库支持
- 实现对话历史
- 集成知识库
- 多模型支持
- API 速率限制

---

## 📊 模板统计

- **支持的平台**：5 个
- **支持的 AI 提供商**：3 个
- **包含的工具模块**：2 个
- **自动生成的行数**：600+
- **节省的开发时间**：8+ 小时

---

## 🏆 为什么使用本模板？

| 功能 | 时间节省 |
|------|---------|
| 项目初始化 | 30 分钟 → 2 分钟 |
| 配置设置 | 20 分钟 → 5 分钟 |
| 基础代码 | 2 小时 → 0 分钟 |
| 总计 | **2.5 小时** |

---

## 📄 许可

本模板和所有相关代码遵循原项目的许可协议。

---

## 🙏 致谢

感谢您使用本模板系统。希望能帮助您快速构建出色的 AI Agent！

---

## 🚀 现在就开始！

```bash
cd template
bash setup_agent.sh my-amazing-agent line
```

**祝您有美好的开发体验！** 💚

---

## 📌 快速参考

```bash
# 创建新项目
bash setup_agent.sh <名称> <平台>

# 配置凭证
nano .env

# 安装依赖
pip install -r requirements.txt

# 验证设置
python check_setup.py

# 启动应用
python main.py

# 生产部署
docker build -t my-agent .
docker run -p 5000:5000 my-agent
```

---

**版本：** 1.0.0  
**最后更新：** 2026-05-03  
**维护者：** OpenClaw 团队
