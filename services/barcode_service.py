import requests

_OPEN_FOOD_FACTS = "https://world.openfoodfacts.org/api/v0/product/{}.json"
_HEADERS = {"User-Agent": "LineBot-LifestyleAssistant/1.0 (educational project)"}


def lookup(barcode: str) -> dict:
    """
    查詢條碼對應的產品資訊。
    資料來源：Open Food Facts（全球食品資料庫，免費無需 API key）。
    回傳 dict，found=True 時包含產品詳情，found=False 時代表查無資料。
    """
    barcode = barcode.strip()
    try:
        resp = requests.get(
            _OPEN_FOOD_FACTS.format(barcode),
            headers=_HEADERS,
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()
    except Exception:
        return {"found": False, "error": "網路連線失敗，請稍後再試"}

    if data.get("status") != 1:
        return {"found": False}

    p = data["product"]
    n = p.get("nutriments", {})

    def _nut(key):
        val = n.get(f"{key}_100g")
        return f"{val:.1f}" if val is not None else None

    return {
        "found": True,
        "barcode": barcode,
        "name": (p.get("product_name_zh")
                 or p.get("product_name_zh-TW")
                 or p.get("product_name_en")
                 or p.get("product_name")
                 or "（未知品名）"),
        "brand": p.get("brands", ""),
        "quantity": p.get("quantity", ""),
        "ingredients": p.get("ingredients_text_zh")
                       or p.get("ingredients_text", ""),
        "allergens": [t.replace("en:", "").replace("zh:", "")
                      for t in p.get("allergens_tags", [])],
        "nutri_score": (p.get("nutriscore_grade") or "").upper(),
        "calories":  _nut("energy-kcal"),
        "fat":       _nut("fat"),
        "saturated": _nut("saturated-fat"),
        "carbs":     _nut("carbohydrates"),
        "sugar":     _nut("sugars"),
        "fiber":     _nut("fiber"),
        "protein":   _nut("proteins"),
        "sodium":    _nut("sodium"),
        "categories": p.get("categories", ""),
    }
