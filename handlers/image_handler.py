from services.vision_service import analyze_image
from prompts.image_prompts import get_prompt
from intent_router import classify_image_intent
import session_store


# 收到圖片時的預設提示文字（用戶未附任何文字）
_DEFAULT_IMAGE_TEXT = "請分析這張圖片"

# 收到圖片後給用戶的引導訊息
GUIDE_MESSAGE = (
    "收到您的圖片！我可以幫您分析：\n"
    "🌿 植物辨識\n"
    "🍽️ 餐點成分與熱量\n"
    "📋 菜單翻譯推薦\n"
    "💊 藥物辨識\n"
    "💆 皮膚 / 醫美分析\n"
    "🏔️ 景色景點辨識\n\n"
    "請直接告訴我您想了解什麼，或我先幫您做通用分析 ⬇️"
)


def handle_new_image(user_id: str, image_bytes: bytes, caption: str = "") -> str:
    """收到新圖片時：儲存圖片，若有文字描述就直接分析，否則引導用戶。"""
    session_store.set_image(user_id, image_bytes)

    if caption.strip():
        intent = classify_image_intent(caption)
        session_store.set_intent(user_id, intent)
        return _run_analysis(image_bytes, intent, caption)

    # 無附帶文字 → 先做通用分析 + 顯示引導
    session_store.set_intent(user_id, "general")
    analysis = _run_analysis(image_bytes, "general", _DEFAULT_IMAGE_TEXT)
    return f"{analysis}\n\n---\n如需特定分析，請告訴我（如「分析熱量」、「辨識植物」）。"


def handle_followup(user_id: str, text: str) -> str:
    """用戶在傳圖後繼續發文字，使用已暫存的圖片進行指定分析。"""
    image_bytes = session_store.get_image(user_id)
    if image_bytes is None:
        return None  # 表示沒有暫存圖片，交由主程式當一般文字處理

    intent = classify_image_intent(text)
    session_store.set_intent(user_id, intent)
    return _run_analysis(image_bytes, intent, text)


def _run_analysis(image_bytes: bytes, intent: str, user_text: str) -> str:
    prompt_cfg = get_prompt(intent)
    # 如果用戶有特定問題，將其附加到 user prompt
    user_prompt = prompt_cfg["user"]
    if user_text and user_text != _DEFAULT_IMAGE_TEXT:
        user_prompt = f"{user_prompt}\n用戶補充：{user_text}"

    return analyze_image(image_bytes, user_prompt, prompt_cfg["system"])
