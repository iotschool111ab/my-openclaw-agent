import os
import requests

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")


def web_search(query: str, max_results: int = 3) -> str:
    """呼叫 Tavily 搜尋，回傳可注入 prompt 的文字摘要。"""
    if not TAVILY_API_KEY:
        return ""
    try:
        resp = requests.post(
            "https://api.tavily.com/search",
            json={"api_key": TAVILY_API_KEY, "query": query, "search_depth": "basic", "max_results": max_results},
            timeout=10,
        )
        results = resp.json().get("results", [])
        if not results:
            return ""
        lines = [f"• {r['title']}：{r['content']}" for r in results]
        return "【即時網路資訊】\n" + "\n".join(lines) + "\n"
    except Exception:
        return ""
