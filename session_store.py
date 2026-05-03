import time

_sessions = {}
IMAGE_TTL = 1800  # 圖片保留 30 分鐘
HISTORY_MAX = 10


def get_session(user_id: str) -> dict:
    if user_id not in _sessions:
        _sessions[user_id] = {
            "last_image_bytes": None,
            "last_image_time": 0,
            "last_intent": None,
            "history": [],
        }
    return _sessions[user_id]


def set_image(user_id: str, image_bytes: bytes):
    s = get_session(user_id)
    s["last_image_bytes"] = image_bytes
    s["last_image_time"] = time.time()


def get_image(user_id: str) -> bytes | None:
    s = get_session(user_id)
    if time.time() - s.get("last_image_time", 0) > IMAGE_TTL:
        s["last_image_bytes"] = None
        return None
    return s.get("last_image_bytes")


def clear_image(user_id: str):
    s = get_session(user_id)
    s["last_image_bytes"] = None
    s["last_image_time"] = 0


def set_intent(user_id: str, intent: str):
    get_session(user_id)["last_intent"] = intent


def get_intent(user_id: str) -> str | None:
    return get_session(user_id).get("last_intent")


def add_history(user_id: str, role: str, content: str):
    history = get_session(user_id)["history"]
    history.append({"role": role, "content": content})
    if len(history) > HISTORY_MAX:
        del history[:-HISTORY_MAX]


def get_history(user_id: str) -> list:
    return get_session(user_id).get("history", [])
