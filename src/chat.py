import requests
import json
import time

MODEL = "qwen2:1.5b" 
MODLE1 = "phi3:3.8b"
MODEL2 = "llama3:8b"
MODEL3 = "deepseek-r1:8b"

TIME_LEDGER = {}

def timer_start(timer_name: str) -> None:
    """Start (or restart) a timer with the given name."""
    TIME_LEDGER[timer_name] = time.perf_counter()
    print(f"Timer '{timer_name}' started.")

def timer_since(timer_name: str) -> float:
    """Return and print elapsed time since a named timer was started."""
    if timer_name not in TIME_LEDGER:
        print(f"Timer '{timer_name}' has not been started.")
        return -1.0

    elapsed_time = time.perf_counter() - TIME_LEDGER[timer_name]
    print(f"Elapsed time for '{timer_name}': {elapsed_time:.2f} seconds")
    return elapsed_time

def timer_reset(timer_name: str) -> None:
    """Reset an existing timer."""
    TIME_LEDGER[timer_name] = time.perf_counter()
    print(f"Timer '{timer_name}' reset.")

def timer_stop(timer_name: str) -> None:
    """Stop (remove) a timer from the ledger."""
    if timer_name in TIME_LEDGER:
        del TIME_LEDGER[timer_name]
        print(f"Timer '{timer_name}' stopped and removed.")
    else:
        print(f"Timer '{timer_name}' not found.")
        

def ask(model,prompt):
    # This is the core of sending the data to the model using .post(url, **kwargs)
    # The "json=" is what the .post() looks out for to know is what being sent to the model
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": model, "prompt": prompt, "stream": False},
        timeout=1000,
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

def chatbot():
    # Setting the stage for the 
    chat_history = [{"role": "system", "content": "You are a helpful assistant. You must remember all messages in this chat and can refer back to them if asked."}]
    print(chat_history)
    prompt_input = input("How can I help you?: ")
    while (prompt_input != "exit" and prompt_input != "0"  ):
        # Adding to the chat history to 
        chat_history.append({"role": "user", "content":prompt_input})

        response = requests.post(
        "http://localhost:11434/api/chat",
        json={"model": MODEL, "messages": chat_history, "stream": False},
        timeout=120,
        )

        
        model_message = response.json()['message']
        chat_history.append(model_message)
        print(model_message["content"])


        prompt_input = input("\nHow can I help you?: ")
        
    return 0

# THIS DOES NOT WORK, DUE TO CPU/RAM LIMITATIONS, GOOD TO HAVE A SERIES OF TEST TO RUN ON EACH MODEL ONE BY ONE AND THEN COMPARE WHILE THE MODEL IS LOADED IN A TERMINAL
def compare(model1, model2, prompt):
    response1 = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": model1, "prompt": prompt, "stream": False},
        timeout=120,
    )
    # Since r is the return JSON from the model in Ollama, then raise_for_status() will 
    response1.raise_for_status()    

    # This basically will just take the r var and convert it to a JSON file using .json() and get the response from the object using ["response"] since it is now a JSON/Dict
    print(model1 + ": " + response1.json()["response"]) 

    response2 = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": model2, "prompt": prompt, "stream": False},
        timeout=120,
    )
    # Since r is the return JSON from the model in Ollama, then raise_for_status() will 
    response2.raise_for_status()    

    # This basically will just take the r var and convert it to a JSON file using .json() and get the response from the object using ["response"] since it is now a JSON/Dict
    print(model2 + ": " + response2.json()["response"])

def temp_ask(model, prompt, temp, seed):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": model,
            "prompt": prompt,
            "temperature": temp,
            "seed": seed,
            "stream": False
        },
        timeout=120,
    )

    response.raise_for_status()
    return response.json()["response"]



if __name__ == "__main__":
    print("Commencing test!")
    prompt = "Can you give me 4 uses for a bobby pin?"
    prompt_list = [
        "Tell me a fun fact about space.",
        "List 5 animals that live in the ocean.",
        "Explain how photosynthesis works in one short paragraph.",
        "Give me three ideas for a healthy breakfast.",
        "What are the main colors in a rainbow?",
        "Write a short joke about cats.",
        "Describe a sunset in one sentence.",
        "What are 5 uses for a paperclip?",
        "Summarize the story of Little Red Riding Hood in 3 sentences.",
        "Explain why the sky looks blue."
        ]

    print("Prompt: " + prompt )
    
    timer_start("whole")
    timer_start("individual")
    for i in range(10):
        timer_reset("individual")
        ask(MODEL,prompt_list[i])
        timer_since("individual")
    
    timer_since("whole")


    #print(temp_ask(MODEL2,prompt,0.5,177))


