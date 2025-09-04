# llm-stomping-ground

A small, clean Python playground for experimenting with open-source LLMs locally using [Ollama](https://ollama.com/).

## 🔧 Requirements

- Python 3.10+
- [Ollama](https://ollama.com/) installed (Windows/macOS/Linux)
- Git (to clone the repo)

## 🚀 Quick Start

1. **Clone the repo**
   ```bash
   git clone https://github.com/Rohan-SP/llm-stomping-ground.git
   cd llm-stomping-ground

2. **Setting up Python environment**
    python -m venv .venv
    .venv\Scripts\Activate.ps1
    pip install -r requirements.txt

3. **Pull the model from Ollama**
    ollama pull qwen2:1.5b

4. **Run Program**
    .venv\Scripts\Activate.ps1 
    python src/chat.py

Project Sturcture
llm-stomping-ground/
├── .venv/
├── src/
│   └── chat.py
├── requirements.txt
├── README.md
└── .gitignore


