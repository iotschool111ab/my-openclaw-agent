"""
意圖辨識模組
回傳 intent 字串，供主程式決定呼叫哪個 handler。

文字 intents：
  route    - Google Maps 路線規劃
  recipe   - 食譜生成
  search   - 需要即時網路搜尋的問題
  chat     - 一般對話

圖片 intents（有圖片時）：
  medical  - 皮膚 / 醫美分析
  medicine - 藥物辨識
  plant    - 植物辨識
  menu     - 菜單翻譯推薦
  food     - 餐點成分熱量分析
  scenery  - 景色景點辨識
  general  - 通用圖片分析（預設）
"""

_ROUTE_KEYWORDS = ["路線", "怎麼去", "導航", "規劃路徑", "地圖", "去哪", "交通方式", "開車去", "搭車去"]
_RECIPE_KEYWORDS = ["食譜", "recipe", "怎麼做", "料理", "製作", "烹飪", "怎麼煮", "做法"]
_SEARCH_KEYWORDS = ["今天", "現在", "最新", "新聞", "天氣", "2024", "2025", "2026", "即時", "最近"]

_IMAGE_INTENT_KEYWORDS = {
    "medical":  ["醫美", "皮膚", "保養", "長痘", "斑點", "暗沉", "毛孔", "整形", "肌膚"],
    "medicine": ["藥", "藥物", "成分", "副作用", "怎麼吃", "藥片", "藥丸", "膠囊"],
    "plant":    ["植物", "花", "樹", "葉子", "這是什麼植物", "草"],
    "menu":     ["菜單", "menu", "點餐", "推薦菜", "這家怎麼點"],
    "food":     ["熱量", "卡路里", "營養", "成分", "食物", "這什麼菜", "餐點", "料理"],
    "scenery":  ["景點", "這是哪", "景色", "在哪裡", "景觀", "旅遊"],
}


def classify_text(text: str) -> str:
    """純文字訊息的意圖分類。"""
    for kw in _ROUTE_KEYWORDS:
        if kw in text:
            return "route"
    for kw in _RECIPE_KEYWORDS:
        if kw in text:
            return "recipe"
    for kw in _SEARCH_KEYWORDS:
        if kw in text:
            return "search"
    return "chat"


def classify_image_intent(text: str) -> str:
    """有圖片時，根據用戶附帶文字決定分析場景；無法判斷則回傳 'general'。"""
    for intent, keywords in _IMAGE_INTENT_KEYWORDS.items():
        for kw in keywords:
            if kw in text:
                return intent
    return "general"
