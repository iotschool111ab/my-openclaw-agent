import os
from dotenv import load_dotenv
load_dotenv()  # 必須在所有自訂模組 import 之前，確保 env 已載入

from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, ImageMessage

import session_store
from intent_router import classify_text
from handlers.maps_handler import handle_route
from handlers.recipe_handler import handle_recipe
from handlers.image_handler import handle_new_image, handle_followup
from services.llm_service import chat
from services.search_service import web_search

load_dotenv()

app = Flask(__name__)
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"


@handler.add(MessageEvent, message=TextMessage)
def handle_text(event):
    user_id = event.source.user_id
    text = event.message.text.strip()

    # 1. 先判斷是否為圖片追問（用戶傳圖後繼續提問）
    followup_resp = handle_followup(user_id, text)
    if followup_resp is not None:
        _reply(event, followup_resp)
        session_store.add_history(user_id, "user", text)
        session_store.add_history(user_id, "assistant", followup_resp)
        return

    # 2. 意圖分類
    intent = classify_text(text)
    history = session_store.get_history(user_id)

    if intent == "route":
        response = handle_route(text)

    elif intent == "recipe":
        response = handle_recipe(text, history)

    elif intent == "search":
        context = web_search(text)
        prompt = f"{context}\n用戶問題：{text}\n請根據以上資訊以繁體中文回答。"
        response = chat(prompt, history=history)

    else:  # chat
        response = chat(text, history=history)

    session_store.add_history(user_id, "user", text)
    session_store.add_history(user_id, "assistant", response)
    _reply(event, response)


@handler.add(MessageEvent, message=ImageMessage)
def handle_image(event):
    user_id = event.source.user_id

    # 下載圖片
    content = line_bot_api.get_message_content(event.message.id)
    image_bytes = b"".join(chunk for chunk in content.iter_content())

    # 先回覆「分析中」避免 LINE 5 秒逾時
    line_bot_api.reply_message(event.reply_token, TextMessage(text="正在分析圖片，請稍候..."))

    # 分析圖片（用 push_message 回傳結果）
    response = handle_new_image(user_id, image_bytes)
    line_bot_api.push_message(user_id, TextMessage(text=response))


def _reply(event, text: str):
    # LINE 單則訊息上限 5000 字元，超過就截斷
    if len(text) > 4900:
        text = text[:4900] + "\n\n（內容過長，已截斷）"
    line_bot_api.reply_message(event.reply_token, TextMessage(text=text))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
