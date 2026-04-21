from .pull_gmail import pull_gmail
from aggregator import build_weekly_narrative
from dotenv import load_dotenv
import json

load_dotenv()

def run_pipeline():
    # 1. INGEST + PROCESS EMAILS
    items = pull_gmail(max_messages=20)

    print(f"[pipeline] extracted {len(items)} items")

    if not items:
        print("[pipeline] no data")
        return []

    # 2. BUILD WEEKLY THEMES
    narratives = build_weekly_narrative(items)

    print(f"[pipeline] generated {len(narratives)} narratives")

    with open("output.json", "w") as f:
        json.dump(narratives, f, indent=2)

    return narratives


if __name__ == "__main__":
    result = run_pipeline()

    for n in result:
        print("\n=== THEME ===")
        print(n["theme"])
        print(n["summary"])
        print("\nHIGHLIGHTS:")
        for h in n["highlights"]:
            print(h)
