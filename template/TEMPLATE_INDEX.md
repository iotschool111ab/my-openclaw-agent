# 模板文件索引

本文件描述了 template 目录中所有文件的用途和使用方式。

## 📂 目录结构

```
template/
├── README.md                    # 模板概述（本文档）
├── QUICK_START.md              # 快速开始指南
├── setup_agent.sh              # 自动化项目生成脚本
├── config.py                   # 配置管理模块
├── requirements.txt            # Python 依赖清单
├── .env.example                # 环境变量示例
├── python_apps/                # Python 应用模板
│   └── minimal_bot.py         # 最小化 Bot 模板
└── utils/                      # 工具模块
    ├── logger.py              # 日志配置
    └── api.py                 # AI API 客户端
```

## 📋 文件说明

### 1. setup_agent.sh ⭐️ **最重要**

**用途：** 自动化生成新的 AI Agent 项目

**使用方法：**
```bash
bash setup_agent.sh <项目名> <平台>
```

**示例：**
```bash
bash setup_agent.sh my-bot line
bash setup_agent.sh telegram-app telegram
bash setup_agent.sh discord-bot discord
```

**功能：**
- ✅ 创建完整的项目目录结构
- ✅ 生成必要的配置文件
- ✅ 复制应用模板
- ✅ 初始化 Git（可选）
- ✅ 显示下一步指导

---

### 2. config.py

**用途：** 集中管理应用的所有配置

**功能：**
- 加载 `.env` 中的环境变量
- 提供类型化的配置访问
- 配置验证

**使用方法：**
```python
from config import config

print(config.PLATFORM)        # 获取平台
print(config.AI_PROVIDER)     # 获取 AI 提供商
print(config.AI_API_KEY)      # 获取 API 密钥
```

**支持的配置项：**
- 应用配置：ENV, DEBUG, LOG_LEVEL, PORT
- 平台配置：PLATFORM, PLATFORM_TOKEN, PLATFORM_SECRET
- AI 配置：AI_PROVIDER, AI_MODEL, AI_API_KEY, AI_TIMEOUT
- 可选：DATABASE_URL, REDIS_URL

---

### 3. requirements.txt

**用途：** 定义项目依赖

**包含的包：**
- Flask 3.0 - Web 框架
- requests - HTTP 客户端
- python-dotenv - 环境变量管理
- Platform SDKs - LINE, Telegram, Discord, Slack
- pydantic - 数据验证
- logging 工具
- 测试工具
- 代码质量工具

**安装方法：**
```bash
pip install -r requirements.txt
```

---

### 4. .env.example

**用途：** 显示所需的环境变量

**如何使用：**
1. 复制到 `.env`：`cp .env.example .env`
2. 编辑填入您的凭证
3. 添加到 `.gitignore` 以避免泄露密钥

**包含部分：**
- 应用配置
- 平台配置（LINE/Telegram/Discord/Slack）
- AI 提供商配置（Groq/OpenAI/Anthropic）
- 可选配置（数据库、缓存等）

---

### 5. python_apps/minimal_bot.py

**用途：** 基础的 Flask Bot 应用模板

**功能：**
- 基础 Flask 服务器
- `/health` 端点 - 健康检查
- `/webhook` 端点 - 接收聊天平台的消息
- `/test` 端点 - 测试 AI 功能
- 错误处理和日志记录

**支持的平台：**
- LINE
- Telegram
- Discord
- Slack

**使用方法：**
```python
# 复制到您的项目
cp template/python_apps/minimal_bot.py ./main.py

# 启动应用
python main.py
```

---

### 6. utils/logger.py

**用途：** 配置应用日志

**功能：**
- 彩色控制台输出
- 文件日志（自动轮转）
- 多级日志支持（DEBUG/INFO/WARNING/ERROR）

**使用方法：**
```python
from utils.logger import setup_logger

logger = setup_logger('my-app', 'INFO')
logger.info("应用启动")
logger.error("发生错误")
```

**特性：**
- 自动创建 `logs` 目录
- 日志文件自动轮转（10MB）
- 保存最多 5 个备份文件

---

### 7. utils/api.py

**用途：** 统一的 AI API 调用接口

**支持的提供商：**
- Groq（推荐，免费）
- OpenAI（付费）
- Anthropic（付费）

**使用方法：**
```python
from utils.api import AIAPIClient

client = AIAPIClient(
    provider='groq',
    model='llama-3.1-8b-instant',
    api_key='your_api_key'
)

response = client.call('Hello, AI!')
print(response)
```

**特性：**
- 统一的 API 接口
- 自动错误处理
- 支持多个提供商
- 可配置的超时时间

---

## 🎯 快速开始步骤

### 步骤 1：生成新项目
```bash
cd template
bash setup_agent.sh my-awesome-bot line
cd my-awesome-bot
```

### 步骤 2：配置
```bash
nano .env
# 填入您的 API 金钥和平台凭证
```

### 步骤 3：安装依赖
```bash
pip install -r requirements.txt
```

### 步骤 4：验证
```bash
python check_setup.py
```

### 步骤 5：启动
```bash
python main.py
```

---

## 🔧 自定义模板

### 修改脚本生成的内容

编辑 `setup_agent.sh`，修改生成的文件内容。

### 添加新平台

1. 编辑 `setup_agent.sh`
2. 在 platform case 语句中添加新平台
3. 定义相应的环境变量和配置

### 扩展 API 客户端

编辑 `utils/api.py`，添加新的 AI 提供商：

```python
def _call_my_provider(self, message: str, **kwargs):
    # 实现您的提供商调用逻辑
    pass
```

---

## 📊 从模板生成的项目结构

运行 `bash setup_agent.sh my-bot line` 后，您将获得：

```
my-bot/
├── main.py                  # 主应用（复制自 minimal_bot.py）
├── config.py               # 配置管理（复制自 config.py）
├── check_setup.py          # 设置检查脚本
├── run.sh                  # 运行脚本
├── .env                    # 环境变量（不提交）
├── .env.example            # 环境变量示例
├── .gitignore              # Git 规则
├── requirements.txt        # 依赖清单（复制自模板）
├── README.md               # 项目 README
├── handlers/               # 消息处理器
│   └── __init__.py
├── utils/                  # 工具模块
│   ├── __init__.py
│   ├── logger.py          # 日志模块（复制自模板）
│   └── api.py             # API 客户端（复制自模板）
└── logs/                   # 日志目录
    └── ai-agent.log
```

---

## ✅ 检查清单

在使用模板前，确保：

- [ ] Bash 已安装（Linux/Mac/WSL）
- [ ] Python 3.8+ 已安装
- [ ] 有效的 AI 提供商 API 密钥
- [ ] 平台凭证（如适用）
- [ ] 网络连接用于 API 调用

---

## 🚀 下一步

完成项目创建后：

1. **测试连接**
   ```bash
   python -c "from utils.api import AIAPIClient; print('✅ Imports OK')"
   ```

2. **测试 AI API**
   ```bash
   python test_ai.py
   ```

3. **配置 Webhook**
   - 在聊天平台获取转发 URL
   - 设置在平台的 Webhook 配置
   - 测试消息流

4. **部署**
   - Docker 容器化
   - 云平台部署
   - 持续集成/部署

---

## 📞 故障排除

### 脚本无法执行
```bash
chmod +x setup_agent.sh
bash setup_agent.sh ...
```

### 模块导入失败
```bash
pip install -r requirements.txt
```

### 环境变量未读取
```bash
# 确保 .env 在项目根目录
python check_setup.py
```

### API 调用失败
```bash
# 检查 API 密钥和网络连接
curl -X POST https://api.groq.com/...
```

---

## 📝 版本历史

**v1.0.0** (2026-05-03)
- ✅ 基础模板系统
- ✅ 多平台支持
- ✅ 自动化生成脚本
- ✅ 工具模块库

---

**准备好了吗？** 前往快速开始指南：[QUICK_START.md](QUICK_START.md)

祝您使用愉快！ 🚀
