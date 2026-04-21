---
name: news-agent
description: Daily tech/AI news curation for thought leadership. Scans sources (TLDR.ai RSS, AI Daily Brief, X #AI #DataGovernance @randyjrouse posts, Substack, LinkedIn via web search), analyzes user's post history (AI/data governance, trust, platforms, Quest ADPF, ITDR from MEMORY.md), generates social posts/video scripts (20-30 sec, executive tone: practical, optimistic, foundation-focused). Use for 'daily news summary', 'content ideas from news', 'generate post on [topic]', or cron automation. Triggers on news/content requests aligned with user's themes.
---

# News Agent

## Core Workflow
1. Pull data (Step 1): Fetch from sources using scripts.
2. Analyze & Curate (Step 2): Match to user voice in references/user_voice.md.
3. Generate Output: 3-5 post ideas + 2 video outlines, tied to Quest if relevant.
4. Automate: Use cron for daily run (8 AM UTC), save to MD, notify.

Keep outputs concise, actionable. Tone: Executive, forward-looking—AI amplifies foundations; weak data fails fast.

## Step 1: Data Pull
Run scripts/ in order:
- `pull_twitter.py`: Recent #AI #DataGovernance + from:@randyjrouse (last 7 days, 10 each).
- `web_linkedin_search.py`: 'Randy Rouse LinkedIn recent posts AI data governance' (top 5).
- RSS: If LINKEDIN_RSS_URL or others set, `parse_rss.py`.
- Fixed: TLDR AI daily (curl https://tldr.tech/ai/rss), AI Daily Brief search, Substack via web_search 'latest AI substack newsletters'.

Save raw to workspace/news-agent-data/[date].json. Filter for relevance (governance, agents, trust).

If no API keys, fallback web_search for all.

## Step 2: Content Generation
Load references/user_voice.md for themes (e.g., 'small trusted data', 'agentic analytics', Gartner ties).
- Match news to 3-5 themes.
- Generate:
  - Posts: Short threads (hook + insight + Quest tie + hashtags #AgenticAI #DataGovernance).
  - Videos: 20-30 sec script (news hook, your angle, CTA).
- Examples in assets/.

For daily: Output to workspace/news-agent-content/[date].md, summarize in chat.

## Automation
Use cron: Daily at 8 AM UTC, run full workflow, send summary if new.

## Resources
- User voice/themes: references/user_voice.md (load for analysis).
- Sources config: references/sources_list.md (URLs, queries).
- Templates: assets/post_template.md, assets/video_template.txt (use as base).

If data empty, say 'No new news—checking tomorrow'.