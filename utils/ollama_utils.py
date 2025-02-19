import requests
import json
import base64
from io import BytesIO

def generate_visual_description(image, detections, api_url, pdf_text):
    # Encode the image to base64
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

    detected_objects = [
        f"{det['class']} (confidence: {det['confidence']:.2f})"
        for det in detections
    ]
    prompt = (
        "[IMG-1] Analyze the image considering both its visual elements and "
        "the following document context. "
        "Detected objects: " + ", ".join(detected_objects) + ". " +
        "Document context: " + pdf_text[:500] + "... " +
        "Generate one concise sentence describing the image's significance."
    )

    payload = {
        "model": "llava:7b",
        "prompt": prompt,
        "images": [img_base64],
        "stream": False
    }

    print("Payload being sent to Ollama:", json.dumps(payload, indent=2))

    try:
        response = requests.post(api_url, json=payload)
        response.raise_for_status()
        result = response.json()

        if "response" in result:
            return result["response"]
        else:
            return f"Unexpected response format: {result}"
    except json.JSONDecodeError:
        return "Error decoding JSON from Ollama API"
    except requests.exceptions.RequestException as e:
        return f"Error generating description: {str(e)}"
