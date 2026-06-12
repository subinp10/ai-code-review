import requests
import os

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def get_pr_diff(repo_full_name: str, pr_number: int) -> str:
    """Fetch the diff/changed files of a pull request."""
    url = f"https://api.github.com/repos/{repo_full_name}/pulls/{pr_number}/files"
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        print(f"❌ Failed to fetch PR files: {response.status_code}")
        return ""

    files = response.json()
    diff_text = ""

    for f in files:
        filename = f.get("filename", "")
        patch = f.get("patch", "")
        if patch:
            diff_text += f"\n\n### File: {filename}\n```\n{patch}\n```"

    return diff_text[:6000]  # Limit to avoid token overflow


def post_review_comment(repo_full_name: str, pr_number: int, review: str):
    """Post a review comment on the pull request."""
    url = f"https://api.github.com/repos/{repo_full_name}/issues/{pr_number}/comments"
    body = f"## 🤖 AI Code Review\n\n{review}\n\n---\n*Reviewed by AI Code Reviewer (M.Tech Project)*"

    response = requests.post(url, headers=HEADERS, json={"body": body})

    if response.status_code == 201:
        print("✅ Comment posted successfully")
    else:
        print(f"❌ Failed to post comment: {response.status_code} - {response.text}")
