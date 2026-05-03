from services.barcode_service import lookup
from services.llm_service import chat
from services.search_service import web_search


def handle_barcode(barcode: str) -> str:
    info = lookup(barcode)

    if not info.get("found"):
        if info.get("error"):
            return info["error"]
        # 查無資料時，用 LLM + 搜尋補救
        context = web_search(f"條碼 {barcode} 產品 成分")
        prompt = (
            f"用戶掃描了條碼 {barcode}，Open Food Facts 查無此產品。\n"
            f"{context}\n"
            "請根據以上資訊（若有）告知用戶，並說明可能原因（如台灣本地產品未收錄）。"
        )
        return chat(prompt, max_tokens=400)

    # 格式化找到的產品資訊
    name      = info["name"]
    brand     = f"品牌：{info['brand']}\n" if info["brand"] else ""
    quantity  = f"容量/重量：{info['quantity']}\n" if info["quantity"] else ""
    score     = f"Nutri-Score：{info['nutri_score']}\n" if info["nutri_score"] else ""

    # 每 100g 營養素
    nut_lines = []
    mapping = [
        ("calories",  "熱量",   "kcal"),
        ("fat",       "脂肪",   "g"),
        ("saturated", "飽和脂肪","g"),
        ("carbs",     "碳水",   "g"),
        ("sugar",     "糖",     "g"),
        ("fiber",     "膳食纖維","g"),
        ("protein",   "蛋白質", "g"),
        ("sodium",    "鈉",     "g"),
    ]
    for key, label, unit in mapping:
        if info.get(key):
            nut_lines.append(f"  {label}：{info[key]} {unit}")

    nutrition = ""
    if nut_lines:
        nutrition = "📊 每 100g 營養素\n" + "\n".join(nut_lines) + "\n"

    allergens = ""
    if info["allergens"]:
        allergens = "⚠️ 過敏原：" + "、".join(info["allergens"]) + "\n"

    ingredients = ""
    if info["ingredients"]:
        ing = info["ingredients"]
        if len(ing) > 300:
            ing = ing[:300] + "..."
        ingredients = f"🧪 成分：{ing}\n"

    summary = (
        f"📦 {name}\n"
        f"{brand}"
        f"{quantity}"
        f"{score}"
        f"\n{nutrition}"
        f"{allergens}"
        f"{ingredients}"
    ).strip()

    # 若有成分資料，讓 LLM 補充健康評估
    if info["ingredients"] or nut_lines:
        prompt = (
            f"以下是掃描到的產品資訊：\n{summary}\n\n"
            "請用繁體中文給出 2-3 句健康評估與飲食建議，簡潔即可。"
        )
        advice = chat(prompt, max_tokens=200)
        return f"{summary}\n\n💡 健康建議\n{advice}"

    return summary
