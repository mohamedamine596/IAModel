import os
import subprocess
import requests
import socket
import sys
import time
import threading

# Ollama setup
OLLAMA_MODEL_DIR = "models"
OLLAMA_MODEL_PATH = os.path.join(OLLAMA_MODEL_DIR, "ollama_model.bin")
MODEL_NAME = "llava:7b"
OLLAMA_DEFAULT_PORT = 11434

loading_flag = [True]

def is_port_in_use(port):
    """Return True if the given TCP port is in use on localhost."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) == 0

def install_ollama():
    """Installs Ollama if not already installed."""
    try:
        subprocess.run(["ollama", "--version"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        os.system("curl -fsSL https://ollama.com/install.sh | sh > /dev/null 2>&1")

def download_model():
    """Attempts to pull the Ollama model silently."""
    if not os.path.exists(OLLAMA_MODEL_PATH):
        try:
            subprocess.run(["ollama", "pull", MODEL_NAME], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            os.makedirs(OLLAMA_MODEL_DIR, exist_ok=True)
            with open(OLLAMA_MODEL_PATH, "w") as f:
                f.write("dummy model content")
        except subprocess.CalledProcessError:
            os.makedirs(OLLAMA_MODEL_DIR, exist_ok=True)
            with open(OLLAMA_MODEL_PATH, "w") as f:
                f.write("dummy model content")

def start_ollama():
    """Starts the Ollama model server silently if not already running."""
    if not is_port_in_use(OLLAMA_DEFAULT_PORT):
        subprocess.Popen(["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def show_loading_animation():
    """Shows a simple loading animation in the terminal."""
    animation = "|/-\\"
    idx = 0
    while loading_flag[0]:
        sys.stdout.write('\rLoading model... ' + animation[idx % len(animation)])
        sys.stdout.flush()
        idx += 1
        time.sleep(0.1)
    sys.stdout.write('\r' + ' ' * 20 + '\r')  # Clear the loading text
    sys.stdout.flush()

def load_ollama_model(silent=True):
    """Silently ensures Ollama is installed, pulls the model if needed, and starts the server."""
    global loading_flag
    loading_flag = [True]
    
    # Start loading animation in a separate thread
    loading_thread = threading.Thread(target=show_loading_animation)
    loading_thread.start()
    
    try:
        install_ollama()
        download_model()
        start_ollama()
    finally:
        loading_flag[0] = False
        loading_thread.join()
    
    return OLLAMA_MODEL_PATH

# Run everything automatically
if __name__ == "__main__":
    load_ollama_model()