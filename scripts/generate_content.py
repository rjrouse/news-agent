#!/usr/bin/env python3
import json
from datetime import datetime

date = datetime.now().strftime('%Y-%m-%d')
data_files = [
    f'/home/node/.openclaw/workspace/news-agent-data/{date}_twitter.json',
    f'/home/node/.openclaw/workspace/news-agent-data/{date}_linkedin.json',
    f'/home/node/.openclaw/workspace/news-agent-data/{date}_rss.json'
]

news = []
for file in data_files:
    if os.path.exists(file):
        with open(file, 'r') as f:
            news.extend(json.load(f).values())  # Flatten

# Load user voice
with open('/home/node/.openclaw/workspace/skills/news-agent/references/user_voice.md', 'r') as f:
    voice = f.read()

# Simple gen (in full, use LLM call or rules)
posts = []
for item in news[:5]:  # Top 5
    title = item.get('title', item.get('text', 'Unknown'))
    posts.append({
        'hook': title,
        'insight': f'This ties to [theme from voice, e.g., AI exposing gaps]. Quest ADPF solves with governed data.',
        'cta': 'What\\'s your take? Link in bio.',
        'hashtags': '#AgenticAI #DataGovernance'
    })

videos = []  # Similar for 20-30 sec

output = {'posts': posts, 'videos': videos, 'voice_summary': voice[:500]}

with open(f'/home/node/.openclaw/workspace/news-agent-content/{date}.md', 'w') as f:
    f.write('# Daily Content Ideas\n')
    for p in posts:
        f.write(f'## Post Idea\n{p["hook"]}\n{p["insight"]}\n{p["cta"]}\n{p["hashtags"]}\n\n')

print(f'Content generated for {date}')