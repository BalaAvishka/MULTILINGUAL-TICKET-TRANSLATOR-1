# Multilingual Ticket Translator

An AI-powered support ticket system that automatically detects the language of incoming tickets, translates them to English for engineers, and translates replies back to the customer's original language — with technical glossary protection.

## Architecture Overview

```
frontend/index.html      ← Single-page UI (vanilla JS)
backend/
  main.py               ← FastAPI REST API
  agent.py              ← Agent Loop (detect → protect → translate → store)
  translator.py         ← Language detection + translation (langdetect + deep-translator)
  glossary.py           ← Technical term protection (API, login, dashboard, etc.)
  storage.py            ← JSON file-based ticket storage
tests/
  test_translator.py    ← Pytest test suite (happy path coverage)
sample_data/            ← Sample tickets in Hindi, Tamil, French, German
```

## AI Capabilities Demonstrated

| Capability | Implementation |
|---|---|
| **Agent Loop** | `agent.py` — 7-step pipeline with recorded steps per ticket |
| **External API Integration** | Google Translate API via `deep-translator` |

## Setup Instructions

### Prerequisites
- Python 3.10+
- pip

### 1. Clone and install
```bash
git clone https://github.com/YOUR_TEAM/multilingual-ticket-translator
cd multilingual-ticket-translator/backend
pip install -r requirements.txt
```

### 2. Run the backend
```bash
cd backend
uvicorn main:app --reload --port 8000
```

### 3. Open the frontend
Open `frontend/index.html` in your browser, OR visit `http://localhost:8000` if you copied index.html into a `frontend/` folder.

### 4. Run tests
```bash
cd tests
pytest test_translator.py -v
```

## Run Instructions

1. Start backend: `uvicorn main:app --reload` from the `backend/` folder
2. Open `http://localhost:8000` in your browser
3. Click a sample language button (Hindi, Tamil, French, etc.)
4. Click "Translate Ticket" — the agent loop runs and shows each step
5. In the reply panel, type your English reply and click "Send Reply"
6. The reply is automatically translated back to the customer's language

## Assumptions & Limitations

- **Translation quality**: Uses Google Translate (free tier via `deep-translator`) — accuracy varies for complex technical language
- **Language detection**: `langdetect` may struggle with very short texts (<10 words)
- **Storage**: JSON files on disk — not suitable for production (replace with SQLite/PostgreSQL)
- **Glossary**: Static list of ~20 common technical terms — extendable via `glossary.py`
- **Rate limits**: Google Translate free tier has usage limits; for production use the paid API
- **No auth**: This prototype has no authentication — add before production deployment

## Deployment (Render.com — Free)

See deployment section in the submission docs.
