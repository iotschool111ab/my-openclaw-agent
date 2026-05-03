"""
意圖辨識模組

文字 intents：
  scan     - LIFF 掃描條碼回傳（前綴 SCAN:）
  menu     - 功能選單
  route    - Google Maps 路線規劃
  recipe   - 食譜生成
  search   - 需要即時網路搜尋
  chat     - 一般對話

圖片 intents（有圖片時）：
  medical / medicine / plant / menu / food / scenery / general
"""

import re

# 關鍵字統一轉小寫比對，方便涵蓋中英混合輸入
_ROUTE_KEYWORDS = [
    "路線", "路程", "路程規劃", "怎麼去", "怎麼走",
    "導航", "規劃路徑", "規劃路線", "地圖", "去哪",
    "交通方式", "開車去", "搭車去", "帶我去",
    "google map", "google maps",          # 英文（小寫比對）
    "map", "directions",
]
_RECIPE_KEYWORDS  = ["食譜", "recipe", "怎麼做", "料理", "製作", "烹飪", "怎麼煮", "做法"]
_SEARCH_KEYWORDS  = ["今天", "現在", "最新", "新聞", "天氣", "2024", "2025", "2026", "即時", "最近"]
_MENU_KEYWORDS    = ["功能", "選單", "能做什麼", "你能做什麼", "help", "幫助", "使用說明"]
_SCAN_KEYWORDS    = ["掃描", "掃條碼", "掃描條碼", "條碼查詢", "掃 qr", "掃qr"]

# 「從 X 到 Y」句型 —— 最可靠的路線判斷
_ROUTE_PATTERN = re.compile(r"從.{1,30}[到至].{1,30}")

_IMAGE_INTENT_KEYWORDS = {
    "medical":  ["醫美", "皮膚", "保養", "長痘", "斑點", "暗沉", "毛孔", "整形", "肌膚"],
    "medicine": ["藥", "藥物", "成分", "副作用", "怎麼吃", "藥片", "藥丸", "膠囊"],
    "plant":    ["植物", "花", "樹", "葉子", "這是什麼植物", "草"],
    "menu":     ["菜單", "menu", "點餐", "推薦菜", "這家怎麼點"],
    "food":     ["熱量", "卡路里", "營養", "成分", "食物", "這什麼菜", "餐點", "料理"],
    "scenery":  ["景點", "這是哪", "景色", "在哪裡", "景觀", "旅遊"],
}


def is_scan_message(text: str) -> bool:
    return text.startswith("SCAN:")


def extract_scan_value(text: str) -> str:
    return text[5:].strip()


def classify_text(text: str) -> str:
    lower = text.lower()

    if is_scan_message(text):
        return "scan"

    for kw in _MENU_KEYWORDS:
        if kw in lower:
            return "menu"

    for kw in _SCAN_KEYWORDS:
        if kw in lower:
            return "open_scan"

    # 路線：關鍵字 + 「從...到...」句型，任一符合即判定
    for kw in _ROUTE_KEYWORDS:
        if kw in lower:
            return "route"
    if _ROUTE_PATTERN.search(text):
        return "route"

    for kw in _RECIPE_KEYWORDS:
        if kw in lower:
            return "recipe"

    for kw in _SEARCH_KEYWORDS:
        if kw in lower:
            return "search"

    return "chat"


def classify_image_intent(text: str) -> str:
    for intent, keywords in _IMAGE_INTENT_KEYWORDS.items():
        for kw in keywords:
            if kw in text:
                return intent
    return "general"
