#  AI GitHub Issue Assistant

An AI-powered assistant that fetches and summarizes GitHub issues using OpenAI’s LLM and FastAPI. Built to help developers quickly understand and take action on GitHub issues across any repository.

---

## Features

-  Fetches latest GitHub issues from any public repository
-  Summarizes issue content using OpenAI GPT models
-  Returns clean, structured JSON responses
-  Frontend built with Vite + React for a fast UI
-  FastAPI backend with OpenRouter or OpenAI integration

---

## 🛠 Tech Stack

| Layer     | Tech Used              |
|-----------|------------------------|
| Backend   | Python, FastAPI        |
| Frontend  | Vite, React, Tailwind  |
| AI Engine | OpenAI GPT / OpenRouter |
| API       | GitHub REST API        |

---

## 📦 Installation & Setup

1. **Clone the repo**  
   ```bash
   git clone https://github.com/basu18-tech/AI-GitHub-Issue-Assistant.git
   cd AI-GitHub-Issue-Assistant
*Backend Setup
pip install -r requirements.txt

*Create a .env file in the root directory:
OPENAI_API_KEY=your_openai_key
GITHUB_TOKEN=your_github_pat

*Run the FastAPI server:
uvicorn main:app --reload

*Frontend Setup
cd frontend
npm install
npm run dev


