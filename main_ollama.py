import os
import base64
import requests
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, ImageMessage
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# 配置區域
LINE_BOT_API = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
HANDLER = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))
OLLAMA_URL = "http://localhost:11434/api/chat"
TAVILY_API_KEY = os.getenv('TAVILY_API_KEY')

def web_search(query):
    """使用 Tavily API 進行連網搜尋"""
    if not TAVILY_API_KEY:
        return ""
    try:
        url = "https://api.tavily.com/search"
        data = {"api_key": TAVILY_API_KEY, "query": query, "search_depth": "basic"}
        response = requests.post(url, json=data, timeout=10)
        results = response.json().get('results', [])
        search_context = "\n".join([f"- {r['title']}: {r['content']}" for r in results[:2]])
        return f"\n【參考網路即時資訊】:\n{search_context}\n"
    except:
        return ""

def smart_model_router(user_input, has_image=False):
    if has_image:
        return {
            "model": "moondream",
            "system": "你是一個專業的視覺分析助手，請使用『繁體中文』簡潔描述這張圖片。",
            "timeout": 120
        }
    
    keywords = ["今天", "現在", "新聞", "天氣", "最新", "2024", "2025", "2026"]
    need_search = any(k in user_input for k in keywords)
    
    return {
        "model": "llama3.2:3b",
        "need_search": need_search,
        "system": "你是一個親切的 AI 助手，請務必使用『繁體中文』回答所有問題。" if not need_search else "你是一個具備連網能力的助手，請根據搜尋結果並使用『繁體中文』回答。",
        "timeout": 60
    }

def call_ollama(message, model, system_prompt, images=None, timeout=60):
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt}, # 強調繁體中文的指令在這裡
            {"role": "user", "content": message}
        ],
        "stream": False,
        "options": {
            "num_ctx": 4096,
            "temperature": 0.6 # 稍微降低溫度可以讓語言輸出更穩定
        }
    }
    if images:
        payload["messages"][1]["images"] = images

    try:
        # 確保發送請求時使用的是這個變數
        response = requests.post(OLLAMA_URL, json=payload, timeout=timeout)
        response.raise_for_status()
        return response.json()['message']['content']
    except requests.exceptions.Timeout:
        return "系統運算時間較長，請再試一次。或是建議您將圖片檔案縮小後再傳送。"


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        HANDLER.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 統一處理所有訊息，刪除原本的 handle_text_message
@HANDLER.add(MessageEvent, message=(TextMessage, ImageMessage))
def handle_unified_message(event):
    user_id = event.source.user_id
    is_image = isinstance(event.message, ImageMessage)
    user_text = event.message.text if not is_image else "請分析這張圖"
    
    # 1. 取得智慧路由設定
    config = smart_model_router(user_text, has_image=is_image)
    
    # 2. 處理搜尋邏輯
    context = ""
    if config.get("need_search"):
        context = web_search(user_text)
    
    # 3. 處理圖片轉碼
    images_payload = None
    if is_image:
        # 針對圖片回覆提示，並使用 Push 異步回覆
        LINE_BOT_API.reply_message(event.reply_token, TextMessage(text="正在切換視覺模型並分析中，請稍候..."))
        msg_content = LINE_BOT_API.get_message_content(event.message.id)
        images_payload = [base64.b64encode(msg_content.content).decode('utf-8')]
    
    # 4. 呼叫模型
    final_prompt = f"{context}\n使用者問題：{user_text}\n請以此資訊為準並以繁體中文回答。"
    
    response = call_ollama(
        message=final_prompt,
        model=config["model"],
        system_prompt=config["system"], # 帶入含有「繁體中文」要求的 System Prompt
        images=images_payload,
        timeout=config["timeout"]
    )

    # 5. 回傳結果
    if is_image:
        LINE_BOT_API.push_message(user_id, TextMessage(text=response))
    else:
        LINE_BOT_API.reply_message(event.reply_token, TextMessage(text=response))

if __name__ == "__main__":
    # 記得先執行: ollama pull llama3.2:3b && ollama pull moondream
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)