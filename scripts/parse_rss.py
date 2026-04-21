#!/usr/bin/env python3
import feedparser
import os
import json
from datetime import datetime

rss_urls = [
    'https://tldr.tech/ai/rss',  # TLDR AI
    # Add more from references/sources_list.md
]

data = {}
for url in rss_urls:
    feed = feedparser.parse(url)
    entries = []
    for entry in feed.entries[:5]:  # Top 5
        entries.append({
            'title': entry.title,
            'link': entry.link,
            'summary': entry.summary[:200] + '...'
        })
    data[url] = entries

date = datetime.now().strftime('%Y-%m-%d')
with open(f'/home/node/.openclaw/workspace/news-agent-data/{date}_rss.json', 'w') as f:
    json.dump(data, f, indent=2)

print(f'RSS data saved for {date}')