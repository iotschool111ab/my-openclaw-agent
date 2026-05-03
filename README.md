# LINE Bot AI 生活助理

以 LINE 為介面的 AI 生活助理，整合 Groq 視覺模型與語言模型，提供圖片分析、路線規劃、食譜生成、即時資訊搜尋等功能。

---

## 功能

| 功能 | 觸發方式 | 說明 |
|------|---------|------|
| 🌿 植物辨識 | 傳圖 + 「植物」/「這是什麼花」 | 辨識種類、習性、是否有毒 |
| 🍽️ 餐點分析 | 傳圖 + 「熱量」/「成分」 | 食材、熱量、營養評分 |
| 📋 菜單翻譯 | 傳圖 + 「菜單」/「推薦什麼」 | 翻譯外文菜單、推薦點餐 |
| 💊 藥物辨識 | 傳圖 + 「藥」/「成分」 | 藥名、成分、用法注意事項 |
| 💆 醫美分析 | 傳圖 + 「皮膚」/「醫美」 | 皮膚狀況評估、保養建議 |
| 🏔️ 景點辨識 | 傳圖 + 「景點」/「這是哪」 | 景點名稱、旅遊建議 |
| 🗺️ 路線規劃 | 「從 A 到 B 的路線」 | 生成開車/大眾運輸/步行 Google Maps 連結 |
| 👨‍🍳 食譜生成 | 「OO 的食譜」/「怎麼做 OO」 | 含食材份量、步驟、技巧 |
| 🔍 即時搜尋 | 含「今天」/「天氣」/「新聞」 | 透過 Tavily 搜尋後回答 |
| 💬 一般對話 | 任意文字 | 帶入對話歷史的 AI 回覆 |

> 傳圖後可繼續追問，Bot 會記住 30 分鐘內的最後一張圖片。

---

## 專案結構

```
my-openclaw-agent/
├── .devcontainer/
│   └── devcontainer.json       # GitHub Codespaces 容器設定
├── handlers/
│   ├── image_handler.py        # 圖片分析分派（含圖片暫存追問）
│   ├── maps_handler.py         # Google Maps 路線連結生成
│   └── recipe_handler.py       # 食譜生成
├── prompts/
│   └── image_prompts.py        # 6 種圖片場景的 system prompt
├── services/
│   ├── llm_service.py          # Groq Chat API（含 OpenClaw Gateway fallback）
│   ├── vision_service.py       # Groq Vision API（含 OpenClaw Gateway fallback）
│   └── search_service.py       # Tavily 即時搜尋
├── main_lifestyle.py           # Flask 主程式（LINE Webhook 入口）
├── intent_router.py            # 意圖辨識（文字 & 圖片場景分類）
├── session_store.py            # 用戶狀態記憶（圖片暫存、對話歷史）
├── requirements.txt
├── .gitignore
├── run_codespace.sh            # GitHub Codespaces 啟動腳本
├── run_local.sh                # 本地 Linux / macOS 啟動腳本
└── run_local.bat               # 本地 Windows 啟動腳本
```

---

## 環境需求

- Python 3.12+
- LINE Messaging API channel
- Groq API key（免費）
- Tavily API key（選用，啟用即時搜尋）
- ngrok（本地端部署使用）

---

## 快速開始

### 1. 設定環境變數

建立 `.env` 檔案（參考下方範本）：

```env
LINE_CHANNEL_ACCESS_TOKEN=你的_line_access_token
LINE_CHANNEL_SECRET=你的_line_channel_secret
GROQ_API_KEY=你的_groq_api_key
TAVILY_API_KEY=你的_tavily_api_key        # 選用
OPENCLAW_GATEWAY_URL=你的_gateway_url     # 選用，Groq 失敗時的備用後端
```

| 金鑰 | 取得方式 | 必填 |
|------|---------|------|
| LINE_CHANNEL_ACCESS_TOKEN | [LINE Developers Console](https://developers.line.biz/) → Messaging API | ✅ |
| LINE_CHANNEL_SECRET | 同上 | ✅ |
| GROQ_API_KEY | [Groq Console](https://console.groq.com/keys) | ✅ |
| TAVILY_API_KEY | [Tavily](https://tavily.com/) | 選用 |
| OPENCLAW_GATEWAY_URL | 自架 OpenAI 相容 Gateway | 選用 |

### 2. 安裝依賴

```bash
pip install -r requirements.txt
```

---

## 執行方式

### GitHub Codespaces

```bash
bash run_codespace.sh
```

腳本會自動顯示 Webhook URL：

```
https://{CODESPACE_NAME}-5000.app.github.dev/callback
```

> **注意**：首次使用 Codespaces 時，請確認 port 5000 已設為 **Public**（Ports 面板中右鍵 → Port Visibility → Public）。建議將金鑰存入 [Codespaces Secrets](https://github.com/settings/codespaces)，不要將 `.env` 提交到 Git。

### 本地端 Windows

```bat
run_local.bat
```

- 自動開新視窗啟動 Flask
- 當前視窗啟動 ngrok，複製顯示的 `Forwarding` HTTPS 網址

### 本地端 Linux / macOS

```bash
bash run_local.sh
```

- Flask 於背景執行，Ctrl+C 時同時關閉
- ngrok 畫面顯示公開 URL

#### ngrok 首次設定（只需一次）

```bash
# macOS
brew install ngrok/ngrok/ngrok

# Windows
winget install ngrok.ngrok

# 設定 auth token（免費帳號即可）
ngrok config add-authtoken <your_token>
```

> Token 取得：[ngrok Dashboard](https://dashboard.ngrok.com/get-started/your-authtoken)

### 3. 設定 LINE Webhook

1. 前往 [LINE Developers Console](https://developers.line.biz/console/)
2. 選擇你的 Messaging API channel
3. 將 Webhook URL 設為：`https://<your-domain>/callback`
4. 點擊 **Verify** 確認連線成功
5. 開啟 **Use webhook** 開關

---

## 使用範例

```
用戶：幫我規劃從台北車站到故宮的路線
Bot：
路線規劃：台北車站 → 故宮博物院

🚗 開車
https://www.google.com/maps/dir/台北車站/故宮博物院/@/@?travelmode=driving

🚇 大眾運輸
https://www.google.com/maps/dir/...?travelmode=transit

🚶 步行
https://www.google.com/maps/dir/...?travelmode=walking
```

```
用戶：[傳一張植物圖片]
Bot：正在分析圖片，請稍候...
Bot：這是「薰衣草（Lavandula angustifolia）」...
     （辨識結果 + 習性 + 照顧方式）

用戶：這個植物有毒嗎？
Bot：（使用暫存的同一張圖片）薰衣草對人類無毒，
     但對貓咪可能造成輕微不適...
```

---

## 架構說明

```
LINE 用戶
    │
    ▼ POST /callback
Flask (main_lifestyle.py)
    │
    ├─ TextMessage
    │       │
    │       ├─ 有暫存圖片？→ image_handler.handle_followup()
    │       │                   └─ Groq Vision API
    │       │
    │       ├─ route   → maps_handler（LLM 萃取地點 + 生成連結）
    │       ├─ recipe  → recipe_handler（Groq Chat）
    │       ├─ search  → Tavily 搜尋 → Groq Chat
    │       └─ chat    → Groq Chat（帶對話歷史）
    │
    └─ ImageMessage
            │
            ├─ reply「分析中...」（避免 LINE 5 秒逾時）
            ├─ 圖片存入 session_store
            └─ Groq Vision 分析 → push_message 回傳結果
```

**AI 後端優先順序：** Groq API → OpenClaw Gateway（fallback）

---

## 已知限制

| 限制 | 說明 | 解法 |
|------|------|------|
| Groq 免費額度 | 每分鐘 token 上限 | 升級 Groq 或設定 OPENCLAW_GATEWAY_URL |
| 無持久化儲存 | 重啟後對話歷史與圖片暫存消失 | 可加入 Redis 持久化 |
| 單一 process | 高流量下回應可能排隊 | 可改用 Gunicorn + 多 worker |
| ngrok 免費版 | 每次重啟 URL 改變 | 升級 ngrok 或使用 Cloudflare Tunnel |

---

## 技術依賴

| 套件 | 用途 |
|------|------|
| Flask | Web 框架 / Webhook 接收 |
| line-bot-sdk | LINE Messaging API |
| requests | HTTP 呼叫 Groq / Tavily |
| python-dotenv | 環境變數載入 |
