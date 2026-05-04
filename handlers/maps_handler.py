import json
import re
import urllib.parse
from services.llm_service import extract_json

# 常見句型：「從 A 到/至 B」、「規劃 A 到 B」、「A 到 B 的路線」
_ROUTE_RE = re.compile(
    r"(?:從|由|自)?\s*(.+?)\s*(?:到|至|前往|去)\s*(.+?)(?:的路線|路線|怎麼去|怎麼走|$)"
)


def _parse_locations(text: str) -> tuple[str, str] | None:
    """從自然語言中抽取出發地與目的地。優先用 regex，失敗才用 LLM。"""
    # 1. regex 優先（速度快、地名不會被 LLM 改寫）
    m = _ROUTE_RE.search(text)
    if m:
        origin = m.group(1).strip()
        dest = m.group(2).strip()
        if origin and dest:
            return origin, dest

    # 2. LLM fallback（針對複雜句型）
    prompt = (
        "從以下句子中提取出發地和目的地，回傳 JSON 格式："
        "{\"origin\": \"...\", \"destination\": \"...\"}。\n"
        "重要規則：\n"
        "- 必須使用繁體中文\n"
        "- 直接複製原句中的地名，絕對不能翻譯、改寫或替換地名\n"
        "- 若無法判斷請回傳 {\"origin\": \"\", \"destination\": \"\"}\n"
        f"句子：{text}"
    )
    raw = extract_json(prompt)
    try:
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
    # 使用 Google Maps 官方 ?api=1 查詢參數格式
    # 中文地名直接放入 URL，不做 percent-encoding，LINE 顯示更友善
    base = "https://www.google.com/maps/dir/?api=1"
    o = urllib.parse.quote(origin, safe="")
    d = urllib.parse.quote(destination, safe="")
    return {
        "driving": f"{base}&origin={o}&destination={d}&travelmode=driving",
        "transit": f"{base}&origin={o}&destination={d}&travelmode=transit",
        "walking": f"{base}&origin={o}&destination={d}&travelmode=walking",
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
