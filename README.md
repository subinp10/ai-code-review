# 🤖 AI Code Reviewer
### M.Tech Project — AI/ML | Computer Science

Automatically reviews GitHub Pull Requests using LLaMA 3 (via Groq API — **100% free**).

---

## 🚀 Setup in 10 Minutes

### Step 1 — Clone & Install
```bash
git clone <your-repo>
cd ai-code-reviewer
pip install -r requirements.txt
```

### Step 2 — Get Free API Keys

**Groq API (Free):**
1. Go to https://console.groq.com
2. Sign up → Create API Key
3. Copy the key

**GitHub Token:**
1. GitHub → Settings → Developer Settings → Personal Access Tokens → Tokens (classic)
2. Generate new token → select `repo` scope
3. Copy the token

### Step 3 — Set Environment Variables
```bash
cp .env.example .env
# Edit .env and fill in your keys
```

### Step 4 — Run the Webhook Server
```bash
uvicorn app.main:app --reload --port 8000
```

### Step 5 — Expose to Internet (for GitHub webhook)
```bash
# Install ngrok from https://ngrok.com (free)
ngrok http 8000
# Copy the https URL e.g. https://abc123.ngrok.io
```

### Step 6 — Set up GitHub Webhook
1. Go to your GitHub repo → Settings → Webhooks → Add webhook
2. Payload URL: `https://abc123.ngrok.io/webhook`
3. Content type: `application/json`
4. Secret: `mysecret` (same as in .env)
5. Events: select **Pull requests**
6. Save

### Step 7 — Run the Dashboard (optional)
```bash
streamlit run dashboard.py
```

---

## 📁 Project Structure
```
ai-code-reviewer/
├── app/
│   ├── main.py          # FastAPI webhook server
│   ├── github_handler.py # GitHub API (fetch diff, post comment)
│   └── reviewer.py       # Groq LLM review engine
├── dashboard.py          # Streamlit UI
├── requirements.txt
└── .env.example
```

---

## 🧪 Testing Without GitHub Webhook
Use the Streamlit dashboard to manually paste code and get reviews instantly.

```bash
streamlit run dashboard.py
```

---

## 📊 For M.Tech Thesis
- Test on 10–15 real open-source PRs
- Compare results with SonarQube (free community edition)
- Document false positives/negatives
- That comparison = your research contribution

---

## Tech Stack
- **LLM:** LLaMA 3 70B via Groq API (free)
- **Backend:** FastAPI + Python
- **GitHub Integration:** GitHub REST API v3
- **UI:** Streamlit
- **Tunneling:** ngrok (free tier)
