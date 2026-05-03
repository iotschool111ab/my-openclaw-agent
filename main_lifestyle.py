import os
from dotenv import load_dotenv
load_dotenv()  # 必須在所有自訂模組 import 之前

from flask import Flask, request, abort, render_template
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, ImageMessage, LocationMessage,
    TextSendMessage, QuickReply, QuickReplyButton, URIAction,
)

import session_store
from intent_router import (
    classify_text, classify_image_intent,
    is_scan_message, extract_scan_value,
)
from handlers.maps_handler import handle_route, handle_route_from_coords
from handlers.recipe_handler import handle_recipe
from handlers.image_handler import handle_new_image, handle_followup
from handlers.barcode_handler import handle_barcode
from services.llm_service import chat
from services.search_service import web_search

app = Flask(__name__)
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

LIFF_LOCATION_ID = os.getenv("LIFF_LOCATION_ID", "")
LIFF_BARCODE_ID  = os.getenv("LIFF_BARCODE_ID", "")

# ── LIFF 頁面路由 ─────────────────────────────────────────────

@app.route("/liff/location")
def liff_location():
    return render_template("liff_location.html", liff_location_id=LIFF_LOCATION_ID)

@app.route("/liff/barcode")
def liff_barcode():
    return render_template("liff_barcode.html", liff_barcode_id=LIFF_BARCODE_ID)

# ── LINE Webhook ──────────────────────────────────────────────

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"


@handler.add(MessageEvent, message=LocationMessage)
def handle_location(event):
    """用戶透過 LIFF 傳送 GPS 位置。"""
    user_id = event.source.user_id
    lat = event.message.latitude
    lng = event.message.longitude
    address = event.message.address or ""

    session_store.set_location(user_id, lat, lng, address)

    # 取得用戶上一個意圖，若是路線規劃則詢問目的地
    reply = (
        f"📍 收到您的位置！\n"
        f"緯度：{lat:.5f}，經度：{lng:.5f}\n\n"
        "請告訴我您要去哪裡，例如：\n「帶我去台北 101」"
    )
    _reply(event, reply)


@handler.add(MessageEvent, message=TextMessage)
def handle_text(event):
    user_id = event.source.user_id
    text = event.message.text.strip()

    # 1. LIFF 條碼掃描回傳（SCAN:xxxxxx）
    if is_scan_message(text):
        barcode = extract_scan_value(text)
        line_bot_api.reply_message(event.reply_token,
            TextSendMessage(text="🔍 條碼查詢中，請稍候..."))
        response = handle_barcode(barcode)
        line_bot_api.push_message(user_id, TextSendMessage(text=response))
        return

    # 2. 圖片追問（用戶上一則有傳圖）
    followup = handle_followup(user_id, text)
    if followup is not None:
        _reply(event, followup)
        session_store.add_history(user_id, "user", text)
        session_store.add_history(user_id, "assistant", followup)
        return

    # 3. 意圖分類
    intent = classify_text(text)
    history = session_store.get_history(user_id)

    if intent == "menu":
        response = _build_menu()

    elif intent == "open_scan":
        response = _build_scan_prompt()

    elif intent == "route":
        # 若有暫存 GPS 位置，詢問目的地後直接帶入座標
        loc = session_store.get_location(user_id)
        if loc and ("到" in text or "去" in text):
            # 嘗試從文字中抽出目的地
            dest = _extract_destination(text)
            if dest:
                response = handle_route_from_coords(loc["lat"], loc["lng"], dest)
            else:
                response = handle_route(text)
        else:
            response = handle_route(text)
            if "無法判斷" in response and LIFF_LOCATION_ID:
                response += f"\n\nhttps://liff.line.me/{LIFF_LOCATION_ID}"

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
    content = line_bot_api.get_message_content(event.message.id)
    image_bytes = b"".join(chunk for chunk in content.iter_content())

    line_bot_api.reply_message(event.reply_token,
        TextSendMessage(text="正在分析圖片，請稍候..."))

    response = handle_new_image(user_id, image_bytes)
    line_bot_api.push_message(user_id, TextSendMessage(text=response))


# ── 輔助函式 ──────────────────────────────────────────────────

def _reply(event, text: str):
    if len(text) > 4900:
        text = text[:4900] + "\n\n（內容過長，已截斷）"
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))


def _extract_destination(text: str) -> str:
    """從「帶我去 XX」「去 XX」之類的句子中抽出目的地（簡單規則）。"""
    import re
    m = re.search(r"(?:去|到|前往|帶我去|導航到)\s*(.+?)(?:的路線|路線|$)", text)
    return m.group(1).strip() if m else ""


def _build_menu() -> str:
    liff_loc  = f"\n   👉 https://liff.line.me/{LIFF_LOCATION_ID}" if LIFF_LOCATION_ID else ""
    liff_scan = f"\n   👉 https://liff.line.me/{LIFF_BARCODE_ID}"  if LIFF_BARCODE_ID  else ""
    return (
        "🤖 LINE 生活助理功能選單\n"
        "══════════════════\n"
        "🗺️ 路線規劃\n"
        "   說：「從 A 到 B 的路線」\n"
        f"   或取得 GPS 位置：{liff_loc}\n\n"
        "🔍 條碼掃描（食品 / 藥品）\n"
        "   說：「掃描條碼」{liff_scan}\n\n"
        "🖼️ 圖片分析（傳圖即可）\n"
        "   植物辨識 / 餐點熱量 / 菜單翻譯\n"
        "   藥物辨識 / 皮膚分析 / 景點辨識\n\n"
        "👨‍🍳 食譜生成\n"
        "   說：「OO 的食譜」\n\n"
        "🔎 即時搜尋\n"
        "   含「今天」「新聞」「天氣」自動搜尋\n\n"
        "💬 一般對話\n"
        "   直接輸入任何問題"
    )


def _build_scan_prompt() -> str:
    if LIFF_BARCODE_ID:
        return (
            "請點擊以下連結開啟條碼掃描器：\n"
            f"https://liff.line.me/{LIFF_BARCODE_ID}\n\n"
            "支援：QR Code、EAN-13、EAN-8、UPC 條碼\n"
            "若相機無法使用，可在掃描頁面手動輸入條碼號碼。"
        )
    return "請先在 .env 設定 LIFF_BARCODE_ID 後重啟服務。"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
