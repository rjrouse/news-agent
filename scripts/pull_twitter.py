#!/usr/bin/env python3
import requests
import os
import json
from datetime import datetime

token = os.environ.get('TWITTER_BEARER_TOKEN')
if not token:
    print('Error: TWITTER_BEARER_TOKEN not set')
    exit(1)

headers = {'Authorization': f'Bearer {token}'}
queries = ['#AI', '#DataGovernance', '#AgenticAI', 'from:randyjrouse']
data = {}

for q in queries:
    params = {'query': q, 'max_results': 10}
    response = requests.get('https://api.twitter.com/2/tweets/search/recent', headers=headers, params=params)
    if response.status_code == 200:
        data[q] = response.json()
    else:
        data[q] = {'error': response.text}

date = datetime.now().strftime('%Y-%m-%d')
with open(f'/home/node/.openclaw/workspace/news-agent-data/{date}_twitter.json', 'w') as f:
    json.dump(data, f, indent=2)

print(f'Twitter data saved for {date}')