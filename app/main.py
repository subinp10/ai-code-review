from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, Request, HTTPException
import hmac, hashlib, os
from app.github_handler import get_pr_diff, post_review_comment
from app.reviewer import review_code

app = FastAPI(title="AI Code Reviewer")

GITHUB_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET", "mysecret")

def verify_signature(payload: bytes, signature: str) -> bool:
    mac = hmac.new(GITHUB_SECRET.encode(), payload, hashlib.sha256)
    return hmac.compare_digest(f"sha256={mac.hexdigest()}", signature)

@app.post("/webhook")
async def github_webhook(request: Request):
    payload_bytes = await request.body()
    sig = request.headers.get("X-Hub-Signature-256", "")

    if not verify_signature(payload_bytes, sig):
        raise HTTPException(status_code=401, detail="Invalid signature")

    event = request.headers.get("X-GitHub-Event")
    payload = await request.json()

    if event == "pull_request" and payload.get("action") in ["opened", "synchronize"]:
        pr_number = payload["pull_request"]["number"]
        repo_full_name = payload["repository"]["full_name"]

        print(f"📥 PR #{pr_number} received from {repo_full_name}")

        diff = get_pr_diff(repo_full_name, pr_number)
        if not diff:
            return {"status": "no diff found"}

        review = review_code(diff)
        post_review_comment(repo_full_name, pr_number, review)

        print(f"✅ Review posted on PR #{pr_number}")
        return {"status": "review posted"}

    return {"status": "event ignored"}

@app.get("/")
def root():
    return {"message": "AI Code Reviewer is running 🚀"}
