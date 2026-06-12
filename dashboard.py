import streamlit as st
import requests
import os
from app.reviewer import review_code

st.set_page_config(page_title="AI Code Reviewer", page_icon="🤖", layout="wide")

st.title("🤖 AI Code Reviewer Dashboard")
st.caption("M.Tech Project — Powered by Groq + LLaMA 3")

st.divider()

# --- Manual Review Section ---
st.subheader("🔍 Manual Code Review")
st.write("Paste any code snippet or diff below to get an instant AI review.")

code_input = st.text_area("Paste your code or diff here:", height=300,
                           placeholder="Paste code or git diff here...")

if st.button("🚀 Review Code", type="primary"):
    if code_input.strip():
        with st.spinner("Analyzing with LLaMA 3 via Groq..."):
            review = review_code(code_input)
        st.success("Review complete!")
        st.markdown(review)
    else:
        st.warning("Please paste some code first.")

st.divider()

# --- GitHub PR Review Section ---
st.subheader("🐙 Review a GitHub PR")
st.write("Enter a GitHub PR link to fetch and review it directly.")

col1, col2 = st.columns(2)
with col1:
    repo = st.text_input("Repository (e.g. owner/repo)", placeholder="torvalds/linux")
with col2:
    pr_num = st.number_input("PR Number", min_value=1, step=1)

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")

if st.button("📥 Fetch & Review PR"):
    if repo and pr_num:
        with st.spinner("Fetching PR diff from GitHub..."):
            from app.github_handler import get_pr_diff
            diff = get_pr_diff(repo, int(pr_num))
        if diff:
            st.code(diff[:1000] + "\n... (truncated)", language="diff")
            with st.spinner("Reviewing with AI..."):
                review = review_code(diff)
            st.success("✅ Review Ready!")
            st.markdown(review)
        else:
            st.error("Could not fetch PR. Check repo name, PR number, and GITHUB_TOKEN.")
    else:
        st.warning("Please fill in both fields.")

st.divider()

# --- Status ---
st.subheader("⚙️ System Status")
groq_key = os.getenv("GROQ_API_KEY", "")
gh_token = os.getenv("GITHUB_TOKEN", "")

col1, col2, col3 = st.columns(3)
col1.metric("Groq API", "✅ Set" if groq_key else "❌ Missing")
col2.metric("GitHub Token", "✅ Set" if gh_token else "❌ Missing")
col3.metric("Model", "LLaMA 3 70B")

st.caption("Webhook server runs separately via `uvicorn app.main:app`. Use ngrok to expose it to GitHub.")
