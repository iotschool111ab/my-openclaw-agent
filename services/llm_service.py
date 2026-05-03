import os
import requests

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
CHAT_MODEL = "llama-3.1-8b-instant"

# OpenClaw Gateway：提供 OpenAI 相容介面，Groq 失敗時自動切換
OPENCLAW_GATEWAY_URL = os.getenv("OPENCLAW_GATEWAY_URL", "")


def _call_api(url: str, headers: dict, payload: dict, timeout: int) -> str:
    resp = requests.post(url, headers=headers, json=payload, timeout=timeout)
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]


def chat(
    user_message: str,
    system_prompt: str = "你是一位親切的生活助理，請以繁體中文回答所有問題。",
    history: list | None = None,
    max_tokens: int = 800,
    timeout: int = 30,
) -> str:
    messages = [{"role": "system", "content": system_prompt}]
    if history:
        messages.extend(history[-8:])
    messages.append({"role": "user", "content": user_message})

    payload = {
        "model": CHAT_MODEL,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": 0.7,
    }

    # 優先使用 Groq，失敗時 fallback 到 OpenClaw Gateway
    if GROQ_API_KEY:
        try:
            return _call_api(
                GROQ_API_URL,
                {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"},
                payload,
                timeout,
            )
        except requests.exceptions.Timeout:
            return "回應逾時，請稍後再試。"
        except Exception:
            pass  # 進入 fallback

    if OPENCLAW_GATEWAY_URL:
        try:
            gateway_url = OPENCLAW_GATEWAY_URL.rstrip("/") + "/v1/chat/completions"
            return _call_api(
                gateway_url,
                {"Content-Type": "application/json"},
                payload,
                timeout,
            )
        except Exception as e:
            return f"AI 服務暫時無法使用：{e}"

    return "未設定 GROQ_API_KEY 或 OPENCLAW_GATEWAY_URL，請檢查 .env 設定。"


def extract_json(prompt: str, timeout: int = 20) -> str:
    """讓 LLM 從文字中萃取結構化資訊（回傳 JSON 字串）。"""
    return chat(
        prompt,
        system_prompt="你是一個資料萃取助手，只輸出 JSON，不要有任何額外說明。",
        max_tokens=300,
        timeout=timeout,
    )
