# Deployment Guide — Render.com (Free Tier)

## Option 1: Render.com (Recommended — Free)

### Step 1: Push to GitHub
```bash
git add .
git commit -m "Initial: Multilingual Ticket Translator"
git push origin main
```

### Step 2: Create a Render account
Go to https://render.com and sign up with GitHub.

### Step 3: New Web Service
1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Configure:
   - **Name**: multilingual-ticket-translator
   - **Root Directory**: backend
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Click "Create Web Service"
5. Wait ~2 minutes for deployment

### Step 4: Update frontend API URL
In `frontend/index.html`, change:
```js
const API = 'http://localhost:8000';
```
To your Render URL:
```js
const API = 'https://multilingual-ticket-translator.onrender.com';
```

### Step 5: Deploy frontend on GitHub Pages
1. In your repo Settings → Pages
2. Set source: Deploy from branch → main → /docs (or /frontend)
3. Copy index.html to docs/ folder and push
4. Your frontend is live at: `https://YOUR_USERNAME.github.io/multilingual-ticket-translator`

---

## Option 2: Railway.app (Also Free)

```bash
npm install -g @railway/cli
railway login
railway init
railway up
```

---

## Option 3: Local with ngrok (For Demo Day)

```bash
# Terminal 1: Run backend
cd backend
uvicorn main:app --reload --port 8000

# Terminal 2: Expose via ngrok (free account)
ngrok http 8000
```
Copy the ngrok URL (e.g. https://abc123.ngrok.io) and update `const API` in index.html.

---

## Verify Deployment

After deploying, check:
```
GET  https://YOUR_URL/health    → {"status":"ok"}
POST https://YOUR_URL/translate → {"ticket_id":"...","english_text":"..."}
GET  https://YOUR_URL/tickets   → [...]
```
