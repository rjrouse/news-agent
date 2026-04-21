# 🧠 News Agent — Multi-Theme Intelligence Feed

Turn your inbox into a structured, high-signal intelligence feed across AI, Data, Cloud, and Market trends.

This project ingests email newsletters (Gmail), extracts structured insights using LLMs, validates and scores them, and generates a weekly narrative summary — similar to a lightweight Bloomberg-style briefing.

---

## 🚀 What This Does

* Connects to Gmail via IMAP
* Parses and cleans newsletter content
* Extracts structured insights using an LLM
* Validates outputs against a strict schema
* Scores insights based on relevance and quality
* Aggregates into multi-theme narratives
* Outputs a structured JSON intelligence feed

---

## 🧩 Architecture

```
Gmail Inbox
   ↓
pull_gmail.py
   ↓
extractor.py (LLM)
   ↓
validator.py (schema enforcement)
   ↓
normalizer.py (structure cleanup)
   ↓
scorer.py (ranking)
   ↓
aggregator.py (theme grouping)
   ↓
output.json (final intelligence feed)
```

---

## 📂 Project Structure

```
news-agent/
├── scripts/
│   ├── main.py              # Entry point
│   ├── run_pipeline.py      # Pipeline orchestration
│   ├── pull_gmail.py        # Email ingestion
│   ├── extractor.py         # LLM insight extraction
│   ├── validator.py         # Schema validation
│   ├── normalizer.py        # Output normalization
│   └── scorer.py            # Insight scoring
│
├── aggregator.py            # Narrative builder
├── schema.py                # Insight schema definition
├── output.json              # Generated intelligence feed
├── assets/                  # Prompt templates (optional)
├── references/              # Source examples / tuning data
└── SKILL.md                 # OpenClaw skill definition
```

---

## ⚙️ Setup

### 1. Clone Repo

```
git clone https://github.com/rjrouse/news-agent.git
cd news-agent
```

---

### 2. Create Virtual Environment

```
python3 -m venv .venv
source .venv/bin/activate
```

---

### 3. Install Dependencies

```
pip install -r requirements.txt
```

If you don’t have one yet, create:

```
pip install imapclient beautifulsoup4 python-dotenv openai
```

---

### 4. Configure Environment Variables

Create a `.env` file:

```
# Gmail
EMAIL_USERNAME=your_email@gmail.com
EMAIL_PASSWORD=your_app_password

# LLM Provider (example)
OPENAI_API_KEY=your_key
OPENAI_BASE_URL=https://api.x.ai/v1   # if using xAI
MODEL=grok-1                          # or your preferred model
```

⚠️ Use a Gmail **App Password**, not your real password.

---

## ▶️ Running the Pipeline

```
python3 -m scripts.main
```

---

## 📊 Output

Results are saved to:

```
output.json
```

Example:

```
[
  {
    "theme": "AI",
    "summary": "Key developments in AI this week",
    "highlights": [
      "AI startup funding surges...",
      "New enterprise adoption trends...",
      "Major platform shifts..."
    ]
  }
]
```

---

## 🧠 Insight Schema

Each extracted insight follows:

```
{
  "title": string,
  "summary": string,
  "insights": [
    {
      "point": string,
      "why_it_matters": string,
      "implication": string
    }
  ],
  "category": "AI | Data | Cloud | Market",
  "tone": "trend | contrarian | breaking",
  "link": string
}
```

---

## 🛑 Validation Rules

* 2–4 insights per item
* Valid category only (AI, Data, Cloud, Market)
* Valid tone (trend, contrarian, breaking)
* Must include structured reasoning fields

Invalid items are rejected during processing.

---

## 🧪 Common Issues

### ❌ "Missing EMAIL creds"

* Ensure `.env` is loaded correctly
* Confirm variables are accessible via `os.getenv()`

---

### ❌ "Too few insights"

* Email content is low signal (welcome emails, promos)
* Working as expected — these are filtered out

---

### ❌ "Model not found"

* Ensure your model name matches provider
* Example for xAI:

  ```
  MODEL=grok-1
  ```

---

### ❌ API Connection Errors

* Check `OPENAI_BASE_URL`
* Verify DNS/network access
* Confirm API key is valid

---

## 🔧 Roadmap / Next Enhancements

* [ ] Multi-source ingestion (Twitter, RSS, LinkedIn)
* [ ] Daily digest mode
* [ ] Slack / email delivery
* [ ] UI dashboard (Streamlit or React)
* [ ] Historical trend tracking
* [ ] Entity extraction (companies, products, people)
* [ ] Sentiment + market impact scoring

---

## 💡 Vision

This evolves from:

> “newsletter summarizer”

into:

> **personalized intelligence layer for data + AI leaders**

Think:

* curated signal > noise
* structured insight > raw content
* narrative > headlines

---

## 📜 License

MIT (or your preferred license)

---

## 👤 Author

Randy Rouse
Field CTO | Data Intelligence & AI Strategy
