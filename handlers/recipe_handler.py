from services.llm_service import chat

_SYSTEM = (
    "你是一位專業廚師與食譜創作者。請根據用戶需求提供詳細食譜，格式如下：\n"
    "【料理名稱】\n"
    "📝 食材（含份量）\n"
    "👨‍🍳 步驟\n"
    "💡 小技巧\n"
    "⏱️ 所需時間\n"
    "🔢 份數\n"
    "請以繁體中文回答，步驟清晰易懂。"
)


def handle_recipe(text: str, history: list | None = None) -> str:
    return chat(text, system_prompt=_SYSTEM, history=history, max_tokens=1000)
