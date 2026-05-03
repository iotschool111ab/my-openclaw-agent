#!/bin/bash
# AI Agent Quick Setup Script
# 快速创建新的 AI Agent 项目

# 颜色定义
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 函数定义
print_header() {
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}================================${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# 检查参数
if [ $# -lt 2 ]; then
    print_error "缺少必要参数"
    echo ""
    echo "用法: bash setup_agent.sh <项目名称> <平台>"
    echo ""
    echo "示例:"
    echo "  bash setup_agent.sh my-bot line"
    echo "  bash setup_agent.sh my-bot telegram"
    echo ""
    echo "支持的平台: line, telegram, discord, slack, text"
    exit 1
fi

PROJECT_NAME=$1
PLATFORM=$2

# 验证平台
case $PLATFORM in
    line|telegram|discord|slack|text)
        print_success "平台: $PLATFORM"
        ;;
    *)
        print_error "不支持的平台: $PLATFORM"
        exit 1
        ;;
esac

print_header "创建 AI Agent 项目: $PROJECT_NAME"

# 创建项目目录
echo -e "${BLUE}[1/5]${NC} 创建项目目录..."
if [ -d "$PROJECT_NAME" ]; then
    print_error "目录已存在"
    exit 1
fi

mkdir -p "$PROJECT_NAME"
cd "$PROJECT_NAME"

# 创建子目录
echo -e "${BLUE}[2/5]${NC} 创建项目结构..."
mkdir -p handlers utils logs
touch handlers/__init__.py utils/__init__.py

# 创建 .env 文件
echo -e "${BLUE}[3/5]${NC} 创建配置文件..."
cat > .env << EOF
# Application
PLATFORM=$PLATFORM
DEBUG=false
LOG_LEVEL=INFO
PORT=5000

# AI Provider
AI_PROVIDER=groq
AI_MODEL=llama-3.1-8b-instant
AI_API_KEY=your_groq_api_key_here

# Platform Credentials
PLATFORM_TOKEN=your_platform_token_here
PLATFORM_SECRET=your_platform_secret_here
EOF

cp .env .env.example

# 创建 requirements.txt
cat > requirements.txt << 'EOF'
flask==3.0.0
requests==2.31.0
python-dotenv==1.0.0
line-bot-sdk==3.5.0
python-telegram-bot==20.0
discord.py==2.3.0
pydantic==2.0.0
EOF

# 创建主应用
echo -e "${BLUE}[4/5]${NC} 创建应用文件..."
cat > main.py << 'PYEOF'
import os
import logging
from dotenv import load_dotenv
from flask import Flask, request
import requests

load_dotenv()

app = Flask(__name__)

logging.basicConfig(
    level=os.getenv('LOG_LEVEL', 'INFO'),
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

PLATFORM = os.getenv('PLATFORM')
AI_API_KEY = os.getenv('AI_API_KEY')
AI_MODEL = os.getenv('AI_MODEL')

def call_ai_api(message: str) -> str:
    try:
        headers = {
            'Authorization': f'Bearer {AI_API_KEY}',
            'Content-Type': 'application/json'
        }
        data = {
            'model': AI_MODEL,
            'messages': [{'role': 'user', 'content': message}],
            'max_tokens': 500,
            'temperature': 0.7
        }
        response = requests.post(
            'https://api.groq.com/openai/v1/chat/completions',
            headers=headers,
            json=data,
            timeout=30
        )
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        logger.error(f"API 错误: {e}")
        return "抱歉，处理失败"

@app.route('/health', methods=['GET'])
def health():
    return {'status': 'ok', 'platform': PLATFORM}, 200

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json()
        # 在这里添加平台特定的处理逻辑
        return {'status': 'ok'}, 200
    except Exception as e:
        logger.error(f"Webhook 错误: {e}")
        return {'error': str(e)}, 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=os.getenv('DEBUG', 'false').lower() == 'true')
PYEOF

# 创建 check_setup.py
cat > check_setup.py << 'PYEOF'
import os
from dotenv import load_dotenv

load_dotenv()

required_vars = ['PLATFORM_TOKEN', 'AI_API_KEY', 'AI_MODEL']
missing = []

for var in required_vars:
    val = os.getenv(var)
    if not val or val.startswith('your_'):
        missing.append(var)

if missing:
    print("❌ 缺少配置:")
    for var in missing:
        print(f"   - {var}")
else:
    print("✅ 配置完成!")
    print("运行: python main.py")
PYEOF

# 创建 .gitignore
cat > .gitignore << 'EOF'
__pycache__/
*.pyc
.env
.venv/
venv/
logs/
*.log
.DS_Store
EOF

# 创建 README
cat > README.md << EOF
# $PROJECT_NAME

AI Agent for $PLATFORM

## 快速开始

1. 安装依赖
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

2. 配置 .env
   \`\`\`bash
   nano .env
   \`\`\`

3. 验证设置
   \`\`\`bash
   python check_setup.py
   \`\`\`

4. 启动
   \`\`\`bash
   python main.py
   \`\`\`
EOF

print_success "应用文件已创建"

# 创建运行脚本
echo -e "${BLUE}[5/5]${NC} 创建运行脚本..."
cat > run.sh << 'EOF'
#!/bin/bash
set -a
source .env
set +a
python main.py
EOF

chmod +x run.sh
print_success "运行脚本已创建"

echo ""
print_header "✅ 项目创建完成！"
echo ""
echo "下一步:"
echo ""
echo "  1. cd $PROJECT_NAME"
echo "  2. nano .env (填入您的 API 金钥)"
echo "  3. pip install -r requirements.txt"
echo "  4. python check_setup.py"
echo "  5. python main.py"
echo ""
