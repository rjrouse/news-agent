import json
import os
from .schema import INSIGHT_SCHEMA
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("XAI_API_KEY"),
    base_url="https://api.x.ai/v1"
)

def extract_insights(email_content: str):
    prompt = f"""
You are an expert analyst.

category must be exactly ONE of: AI, Data, Cloud, Market. Never combine values.

Extract structured insights in STRICT JSON format:

{INSIGHT_SCHEMA}

Rules:
- No commentary
- No markdown
- Output valid JSON only
- Focus on signal, not summary

EMAIL:
{email_content}
"""

    resp = client.chat.completions.create(
        model="grok-4-fast-non-reasoning",
        messages=[
            {"role": "system", "content": "You extract structured insights."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return json.loads(resp.choices[0].message.content)
