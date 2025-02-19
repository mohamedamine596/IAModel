import requests
import json
import base64
from io import BytesIO

def generate_image_caption(image, api_url, context_text=""):
    """
    Generate a caption for an image using the Ollama model.
    This function sends a request to the Ollama model server to generate a description.
    """
    # Convert image to base64
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

    prompt = "Provide a concise and creative caption for this image."
    if context_text:
        prompt += f" Additional context: {context_text[:500]}..."

    payload = {
        "model": "llava:7b",
        "prompt": prompt,
        "stream": False,
        "images": [img_str]
    }

    print("Payload being sent:", json.dumps(payload, indent=2))

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