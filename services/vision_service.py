import os
import base64
import requests

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
VISION_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"

OPENCLAW_GATEWAY_URL = os.getenv("OPENCLAW_GATEWAY_URL", "")


def analyze_image(image_bytes: bytes, user_prompt: str, system_prompt: str, timeout: int = 60) -> str:
    b64 = base64.b64encode(image_bytes).decode("utf-8")

    payload = {
        "model": VISION_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}},
                    {"type": "text", "text": user_prompt},
                ],
            },
        ],
        "max_tokens": 1200,
        "temperature": 0.5,
    }

    # 優先使用 Groq Vision
    if GROQ_API_KEY:
        try:
            resp = requests.post(
                GROQ_API_URL,
                headers={"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"},
                json=payload,
                timeout=timeout,
            )
            resp.raise_for_status()
            return resp.json()["choices"][0]["message"]["content"]
        except requests.exceptions.Timeout:
            return "圖片分析逾時，請稍後再試或縮小圖片後重傳。"
        except Exception:
            pass  # fallback

    # Fallback：OpenClaw Gateway（需支援視覺模型）
    if OPENCLAW_GATEWAY_URL:
        try:
            gateway_url = OPENCLAW_GATEWAY_URL.rstrip("/") + "/v1/chat/completions"
            resp = requests.post(
                gateway_url,
                headers={"Content-Type": "application/json"},
                json=payload,
                timeout=timeout,
            )
            resp.raise_for_status()
            return resp.json()["choices"][0]["message"]["content"]
        except Exception as e:
            return f"圖片分析失敗：{e}"

    return "未設定 GROQ_API_KEY 或 OPENCLAW_GATEWAY_URL，請檢查 .env 設定。"
