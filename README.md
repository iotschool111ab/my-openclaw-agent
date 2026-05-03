# my-openclaw-agent
My first autonomous AI agent powered by OpenClaw, integrated with LINE BOT for file and image uploads.

## 功能特色

- **文字訊息處理**：接收使用者文字訊息並由 Groq AI 回應
- **圖片上傳**：下載並處理使用者上傳的圖片
- **檔案上傳**：下載並處理使用者上傳的檔案
- **免費 Groq API**：使用免費的 Groq Llama 3.1 8B Instant 模型

## 快速開始

1. **安裝依賴**：
   ```bash
   pip install -r requirements.txt
   ```

2. **配置環境變數**：
   - 在 `.env` 文件中設置您的 LINE BOT 憑證和 Groq API key
   - LINE 憑證從 https://developers.line.biz/ 獲取
   - Groq API key 從 https://console.groq.com/keys 獲取

3. **檢查設置**：
   ```bash
   python check_setup.py
   ```

4. **運行應用**：
   - **完整版本** (推薦)：`./run.sh`
   - **簡單版本** (免費層友好)：`./run_simple.sh`

5. **設置 Webhook**：
   - 使用 ngrok 暴露本地端口：`ngrok http 5000`
   - 在 LINE Console 中設置 webhook URL

## 運行

### 選項 1: 完整 OpenClaw Agent (推薦，但可能有速率限制)
```bash
./run.sh
```

### 選項 2: 簡單 Groq API (繞過速率限制)
```bash
./run_simple.sh
```

簡單版本直接調用 Groq API，適合免費層使用，但功能較少。

### 本地開發
使用 ngrok 暴露端口 5000：
```bash
ngrok http 5000
```
在 LINE Developers Console 中設置 webhook URL 為 `https://your-ngrok-url.ngrok.io/callback`

## Features

- Receive text messages from LINE users
- Handle image uploads and process them with OpenClaw AI
- Handle file uploads and process them with OpenClaw AI
- Reply with AI-generated responses

## 已知限制

**Groq 免費層限制：**
- 免費層有 6000 tokens/minute (TPM) 限制
- OpenClaw 預設發送大量工具定義，可能超過限制
- 如果遇到 "Request too large" 錯誤，請：

### 解決方案：

1. **升級到 Groq Dev Tier：**
   - 訪問 https://console.groq.com/settings/billing
   - 升級到付費層以獲得更高限制

2. **使用替代免費模型：**
   - 考慮使用其他免費 AI 提供者
   - 或等待速率限制重置

3. **減少工具使用：**
   - 應用目前使用完整 OpenClaw 工具套件
   - 可以修改為使用更簡單的模式
