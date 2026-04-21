def normalize_insight(insight: dict, metadata: dict) -> dict:
    return {
        "title": insight.get("title", "").strip(),
        "summary": insight.get("summary", "").strip(),
        "insights": [
            i.strip() for i in insight.get("insights", [])
            if isinstance(i, str) and i.strip()
        ],
        "url": metadata.get("url"),
        "source": metadata.get("source", "gmail")
    }
