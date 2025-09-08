import requests
import json

MODEL = "qwen2:1.5b"  # or "phi3:3.8b"

def ask(prompt: str) -> str:
    # This is the core of sending the data to the model using .post(url, **kwargs)
    # The "json=" is what the .post() looks out for to know is what being sent to the model
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": MODEL, "prompt": prompt, "stream": False},
        timeout=120,
    )
    # Since r is the return JSON from the model in Ollama, then raise_for_status() will 
    response.raise_for_status()    

    # This basically will just take the r var and convert it to a JSON file using .json() and get the response from the object using ["response"] since it is now a JSON/Dict
    return response.json()["response"]

# This works but I may need to have a custom UI  
def stream_ask(prompt: str) -> str:

    stream_response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": MODEL, "prompt": prompt, "stream": True},
        timeout=120,
    )
    
    stream_response.raise_for_status()    
    count = 0
    for line in stream_response.iter_lines():
        if line:
            data = json.loads(line.decode("utf-8"))
            print(data["response"], end="", flush=True)

def loop():
    prompt_input = ""
    while (prompt_input != "exit" or prompt_input != "0"  ):
        prompt_input = input("What would you like to ask the model?: ")


    return 0


if __name__ == "__main__":
    ask_model = "Explain how a rocket works, in 25 paragraphs"
    print("will now start streaming response")
    print(ask(ask_model))
