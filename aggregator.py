from collections import defaultdict

def aggregate_insights(items):
    clusters = defaultdict(list)

    for item in items:
        insight = item["insight"]
        score = item["score"]["score"]

        text = (
            insight.get("title", "") + " " +
            insight.get("summary", "")
        ).lower()

        # naive topic clustering (MVP)
        if "ai" in text:
            clusters["AI"].append(item)
        elif "data" in text:
            clusters["Data Infrastructure"].append(item)
        elif "security" in text:
            clusters["Security"].append(item)
        else:
            clusters["General"].append(item)

    return clusters

def build_narrative(cluster_name, items):
    sorted_items = sorted(items, key=lambda x: x["score"]["score"], reverse=True)

    bullets = []
    for item in sorted_items[:5]:
        i = item["insight"]
        bullets.append(f"- {i['summary']}")

    return {
        "theme": cluster_name,
        "summary": f"Key developments in {cluster_name} this week",
        "highlights": bullets
    }

def build_weekly_narrative(all_items):
    clusters = aggregate_insights(all_items)

    narratives = []

    for name, items in clusters.items():
        if len(items) < 2:
            continue  # avoid weak signals

        narratives.append(build_narrative(name, items))

    return narratives
