def score_insight(insight: dict) -> dict:
    score = 0.0
    reasons = []

    text = (insight.get("summary", "") + " " +
            " ".join(insight.get("insights", []))).lower()

    # signal boosters
    keywords = {
        "ai": 0.2,
        "launch": 0.2,
        "announced": 0.15,
        "acquisition": 0.25,
        "funding": 0.25,
        "regulation": 0.2
    }

    for k, v in keywords.items():
        if k in text:
            score += v
            reasons.append(f"keyword:{k}")

    # structure quality
    if len(insight.get("insights", [])) >= 3:
        score += 0.1
        reasons.append("structured_insights")

    if len(insight.get("summary", "")) > 100:
        score += 0.1
        reasons.append("rich_summary")

    return {
        "score": min(score, 1.0),
        "reasons": reasons
    }
