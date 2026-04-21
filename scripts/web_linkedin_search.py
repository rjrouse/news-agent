#!/usr/bin/env python3
import requests
from datetime import datetime
import json
import re

query = 'Randy Rouse LinkedIn recent posts AI data governance'
# Use DuckDuckGo API or scrape (fallback to simple search)
url = f'https://api.duckduckgo.com/?q={query}&format=json&no_html=1&skip_disambig=1'

response = requests.get(url)
if response.status_code == 200:
    results = response.json()['RelatedTopics'][:5]  # Top 5
    parsed = []
    for r in results:
        title = r.get('Text', '')
        link = r.get('FirstURL', '')
        parsed.append({'title': title, 'link': link})
else:
    parsed = [{'error': 'Search failed'}]

date = datetime.now().strftime('%Y-%m-%d')
with open(f'/home/node/.openclaw/workspace/news-agent-data/{date}_linkedin.json', 'w') as f:
    json.dump(parsed, f, indent=2)

print(f'LinkedIn search saved for {date}')