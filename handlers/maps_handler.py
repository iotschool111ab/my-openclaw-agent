import json
import re
import urllib.parse
from services.llm_service import extract_json


def _parse_locations(text: str) -> tuple[str, str] | None:
    """用 LLM 從自然語言中抽取出發地與目的地，失敗時回傳 None。"""
    prompt = (
        f"從以下句子中提取出發地和目的地，回傳 JSON 格式：{{\"origin\": \"...\", \"destination\": \"...\"}}。\n"
        f"若無法判斷請回傳 {{\"origin\": \"\", \"destination\": \"\"}}。\n"
        f"句子：{text}"
    )
    raw = extract_json(prompt)
    try:
        # 只取第一個 JSON 物件
        match = re.search(r"\{.*?\}", raw, re.DOTALL)
        if not match:
            return None
        data = json.loads(match.group())
        origin = data.get("origin", "").strip()
        dest = data.get("destination", "").strip()
        if not origin or not dest:
            return None
        return origin, dest
    except Exception:
        return None


def _build_urls(origin: str, destination: str) -> dict[str, str]:
    o = urllib.parse.quote(origin)
    d = urllib.parse.quote(destination)
    base = f"https://www.google.com/maps/dir/{o}/{d}"
    return {
        "driving": f"{base}/@/@?travelmode=driving",
        "transit": f"{base}/@/@?travelmode=transit",
        "walking": f"{base}/@/@?travelmode=walking",
    }


def handle_route(text: str) -> str:
    result = _parse_locations(text)
    if result is None:
        return (
            "無法判斷出發地或目的地，請說得更清楚一點。\n"
            "例如：「幫我規劃從台北車站到故宮的路線」\n\n"
            "或點選下方按鈕取得您的 GPS 位置作為出發地 👇"
        )

    origin, destination = result
    return _format_route(origin, destination)


def handle_route_from_coords(lat: float, lng: float, destination: str) -> str:
    """以 GPS 座標為出發地規劃路線。"""
    origin_coord = f"{lat},{lng}"
    origin_label = "您的目前位置"
    urls = _build_urls(origin_coord, destination)

    return (
        f"路線規劃：{origin_label} → {destination}\n\n"
        f"🚗 開車\n{urls['driving']}\n\n"
        f"🚇 大眾運輸\n{urls['transit']}\n\n"
        f"🚶 步行\n{urls['walking']}"
    )


def _format_route(origin: str, destination: str) -> str:
    urls = _build_urls(origin, destination)
    return (
        f"路線規劃：{origin} → {destination}\n\n"
        f"🚗 開車\n{urls['driving']}\n\n"
        f"🚇 大眾運輸\n{urls['transit']}\n\n"
        f"🚶 步行\n{urls['walking']}"
    )
