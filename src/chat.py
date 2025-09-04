import requests

MODEL = "qwen2:1.5b"  # or "phi3:3.8b"

def ask(prompt: str) -> str:
    r = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": MODEL, "prompt": prompt, "stream": False},
        timeout=120,
    )
    r.raise_for_status()
    return r.json()["response"]

if __name__ == "__main__":
    print(ask("Hello! Explain what a token is in LLMs."))
