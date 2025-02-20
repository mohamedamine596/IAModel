# utils/image_utils.py
import requests
import json
import re

def generate_image_caption(input_data, api_url, context_text=""):
    """
    Generate a detailed caption for an image using the provided input data and optional context.
    """
    prompt = """Provide a detailed and creative caption for the image. 
    Include visual elements, mood, actions, and setting. 
    Aim for 2-3 sentences that tell a story about what you see."""
    
    if context_text:
        prompt += f"Additional context: {context_text[:500]}..."

    payload = {
        "model": "llava:7b",
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(api_url, json=payload)
        response.raise_for_status()

        result = response.json()
        if "response" in result:
            caption = result["response"]
            cleaned_caption = re.sub(r"^[^A-Za-z]+", "", caption.strip())
            return cleaned_caption
        else:
            return f"Error: Unexpected response format"
    except (json.JSONDecodeError, requests.exceptions.RequestException) as e:
        return f"Error: {str(e)}"