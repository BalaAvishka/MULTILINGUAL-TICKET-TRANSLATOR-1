# AI Usage Note — Multilingual Ticket Translator

## What AI Helped With
- Scaffolding the FastAPI project structure and endpoint design
- Writing the agent loop logic in `agent.py` with step-by-step recording
- Designing the glossary protection + restore pattern for technical terms
- Writing pytest test cases covering the happy path and edge cases
- Generating sample tickets in Hindi, Tamil, French, and German
- Frontend HTML/CSS layout and JS for the two-panel ticket interface
- Writing the README architecture overview

## What AI Got Wrong / Needed Correction
- Initial agent loop was too simple (no step recording) — prompted to add step-by-step logging
- First glossary approach used regex which broke on partial matches — corrected to exact string replace with unique placeholders
- Frontend initially used `fetch` without proper error handling — added try/catch and status messages
- `deep_translator` import syntax was slightly different from what AI suggested — corrected based on docs

## Best Prompts Used

1. **Agent loop design:**
   > "Build a 7-step agent loop in Python that detects language, protects technical terms with placeholders, translates, restores terms, and records each step. Return the full step log with the result."

2. **Glossary pattern:**
   > "Write a Python function that replaces technical terms (API, login, dashboard, error 404) with unique placeholders before translation, then restores them after. Make it round-trip safe."

3. **Test cases:**
   > "Write pytest tests covering: glossary round-trip, language detection for English/Hindi/French, agent happy path producing required fields, reply translation, and error handling for missing tickets."

4. **Frontend:**
   > "Build a single HTML file support ticket tool with: left panel to submit tickets with language auto-detection, right panel showing ticket queue, bottom panel for engineer replies that translate back. Use vanilla JS with fetch calls to a FastAPI backend."

5. **README:**
   > "Write a README with setup instructions, run instructions, architecture overview, and assumptions & limitations for a multilingual ticket translator using FastAPI + langdetect + deep-translator."
