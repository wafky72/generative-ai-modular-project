# 🤖 AI_Agent

A lightweight, modular AI Agent built by me as a personal project.  
This repository contains the core logic and components for an AI-powered agent that can be extended to perform various tasks like data processing, chatbot interactions, document querying, or workflow automation.

---

## 🚀 Features

- Modular architecture (easy to plug in new tools and logic)
- Supports local or cloud-based LLMs (OpenAI, HuggingFace, etc.)
- Simple and extendable agent loop
- Basic memory and context tracking
- CLI interface (with future plans for web UI)
- Can be used for:
  - Question answering from documents
  - Task automation
  - Interactive chat or support bot

---

## 🧠 Tech Stack

- Python 3.10+
- LangChain / OpenAI / LlamaIndex (optional integrations)
- FastAPI (optional for web endpoints)
- FAISS or Chroma for vector memory
- dotenv for managing environment variables

---

## 📦 Getting Started

```bash
# Clone the repo
git clone (https://github.com/wafky72/generative-ai-modular-project)
cd generative-ai-modular-project

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install agno
pip install google-genai
pip install duckduckgo-search
pip install streamlit
