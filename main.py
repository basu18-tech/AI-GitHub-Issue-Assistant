from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

#  Load environment variables
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
github_token = os.getenv("GITHUB_TOKEN")

print(" Loaded OPENAI_API_KEY:", openai_api_key[:10])
print(" Loaded GITHUB_TOKEN:", github_token[:10])

#  FastAPI App Setup
app = FastAPI(
    title="GitHub Issue Analyzer",
    description="Analyze GitHub issues using GPT",
    version="1.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#  Request Model
class IssueRequest(BaseModel):
    owner: str
    repo: str
    issue_number: int


#  Fetch Issue from GitHub
def fetch_issue(owner, repo, issue_number):
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}"
    headers = {
        "Authorization": f"Bearer {github_token}"
    }
    print("🔗 Fetching issue:", url)
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"GitHub Error {response.status_code}: {response.text}")
    return response.json()


# Analyze with OpenRouter GPT
def analyze_with_gpt(issue_data):
    if not openai_api_key:
        raise Exception(" OPENAI_API_KEY is missing from environment variables.")

    prompt = f"Issue Title: {issue_data.get('title')}\n\nDescription:\n{issue_data.get('body', '')}"

    headers = {
        "Authorization": f"Bearer {openai_api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "system",
                "content": "You are an assistant that analyzes GitHub issues and provides summaries and suggestions."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.3
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)

    if response.status_code != 200:
        raise Exception(f"OpenAI Error: Error code: {response.status_code} - {response.text}")

    return response.json()["choices"][0]["message"]["content"]


@app.post("/analyze_issue/")
def analyze_issue(issue: IssueRequest):
    try:
        issue_data = fetch_issue(issue.owner, issue.repo, issue.issue_number)
        analysis = analyze_with_gpt(issue_data)
        return {"analysis": analysis}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"❌ {str(e)}"})
