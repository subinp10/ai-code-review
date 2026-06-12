import os
import requests

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.3-70b-versatile"  # Free on Groq

SYSTEM_PROMPT = """You are an expert code reviewer. When given a Git diff (code changes from a pull request), analyze the changes and provide a structured review covering:

1. 🐛 **Bugs & Logic Errors** — Any potential bugs, null pointer issues, off-by-one errors, etc.
2. 🔒 **Security Issues** — Hardcoded credentials, SQL injection, XSS, insecure practices.
3. ⚡ **Performance** — Inefficient loops, unnecessary DB calls, memory issues.
4. 🎨 **Code Style & Best Practices** — Naming conventions, code duplication, readability.
5. ✅ **Positive Feedback** — What was done well.

Be specific, cite line numbers or code snippets where possible, and keep the tone constructive and helpful.
If the diff is trivial or has no issues, say so clearly."""

def review_code(diff: str) -> str:
    """Send code diff to Groq LLM and return review."""
    if not GROQ_API_KEY:
        return "❌ GROQ_API_KEY not set. Please add it to your .env file."

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Please review the following code changes:\n\n{diff}"}
        ],
        "temperature": 0.3,
        "max_tokens": 1500
    }

    try:
        response = requests.post(GROQ_URL, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"❌ Groq API error: {e}")
        return f"❌ Review failed: {str(e)}"
