import os
import subprocess
import sys
import json
import requests
import socket

# Ollama setup
OLLAMA_MODEL_DIR = "models"
OLLAMA_MODEL_PATH = os.path.join(OLLAMA_MODEL_DIR, "ollama_model.bin")
MODEL_NAME = "llava:7b" 
OLLAMA_DEFAULT_PORT = 11434

def is_port_in_use(port):
    """Return True if the given TCP port is in use on localhost."""
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) == 0

def install_ollama():
    """Installs Ollama if not already installed."""
    try:
        subprocess.run(["ollama", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Ollama is already installed.")
    except FileNotFoundError:
        print("Installing Ollama...")
        os.system("curl -fsSL https://ollama.com/install.sh | sh")
        print("Ollama installation complete.")

def download_model():
    """Attempts to pull the Ollama model, falling back to a dummy model if needed."""
    if not os.path.exists(OLLAMA_MODEL_PATH):
        print("Ollama model not found locally. Pulling it using the 'ollama pull' command...")
        try:
            subprocess.run(["ollama", "pull", MODEL_NAME], check=True)
            print("Ollama model pulled successfully.")
            # For simulation purposes, create a dummy file to represent the pulled model.
            os.makedirs(OLLAMA_MODEL_DIR, exist_ok=True)
            with open(OLLAMA_MODEL_PATH, "w") as f:
                f.write("dummy model content pulled from ollama")
        except subprocess.CalledProcessError as e:
            # If pulling fails, fall back to using a dummy model.
            print(f"Error pulling Ollama model: {e}")
            print("Using fallback dummy model for testing purposes.")
            os.makedirs(OLLAMA_MODEL_DIR, exist_ok=True)
            with open(OLLAMA_MODEL_PATH, "w") as f:
                f.write("dummy model content fallback")
    else:
        print("Local Ollama model found.")

def start_ollama():
    """Starts the Ollama model server if not already running."""
    if is_port_in_use(OLLAMA_DEFAULT_PORT):
        print(f"Ollama model server already running on port {OLLAMA_DEFAULT_PORT}.")
        return
    print("Starting Ollama model server...")
    subprocess.Popen(["ollama", "serve"])
    print("Ollama model server started.")

def load_ollama_model():
    """Ensures Ollama is installed, pulls the model if needed, and starts the server."""
    install_ollama()
    download_model()
    start_ollama()
    return OLLAMA_MODEL_PATH

def generate_visual_description(image, detections, api_url, context_text=""):
    """
    Generate a detailed textual description of the image using the Ollama model.
    If detections list is empty, a generic prompt is used.
    Optionally include additional context (e.g. extracted PDF text).
    """
    if detections:
        detected_info = ", ".join([det["class"] for det in detections])
        prompt = f"Please provide a detailed and creative description of the image containing these objects: {detected_info}. "
    else:
        prompt = "Please provide a detailed and creative description of the image. "
    if context_text:
        prompt += f"Additional context: {context_text[:500]}..."
    
    payload = {
        "model": MODEL_NAME,  # Update if needed.
        "prompt": prompt,
        "stream": False
    }
    
    print("Payload being sent to Ollama model:", json.dumps(payload, indent=2))
    
    try:
        response = requests.post(api_url, json=payload)
        response.raise_for_status()
        result = response.json()
        if "response" in result:
            return result["response"]
        else:
            return f"Unexpected response format: {result}"
    except json.JSONDecodeError:
        return "Error decoding JSON"
    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"

# Run everything automatically
if __name__ == "__main__":
    load_ollama_model()
