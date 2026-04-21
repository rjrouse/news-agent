# workspace/skills/news-agent/schema.py

from typing import List, TypedDict


class InsightItem(TypedDict):
    point: str
    why_it_matters: str
    implication: str


class InsightOutput(TypedDict):
    title: str
    summary: str
    insights: List[InsightItem]
    category: str   # AI | Data | Cloud | Market
    tone: str       # trend | contrarian | breaking
    link: str

VALID_CATEGORIES = {"AI", "Data", "Cloud", "Market"}
VALID_TONES = {"trend", "contrarian", "breaking"}
MAX_INSIGHTS = 4
MIN_INSIGHTS = 1

def empty_insight() -> InsightOutput:
    return {
        "title": "",
        "summary": "",
        "insights": [],
        "category": "",
        "tone": "",
        "link": ""
    }

INSIGHT_SCHEMA = {
    "title": "string",
    "summary": "string",
    "insights": [
        {
            "point": "string",
            "why_it_matters": "string",
            "implication": "string"
        }
    ],
    "category": "AI | Data | Cloud | Market",
    "tone": "trend | contrarian | breaking",
    "link": "string"
}
