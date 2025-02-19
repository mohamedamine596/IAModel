import requests
import json

def generate_image_caption(detections, api_url, context_text=""):
    """
    Generate a caption for an image using the detected objects and optional context.
    This function sends a request to the Ollama model server to generate a description.
    """
    detected_objects = ", ".join([
        f"{det['class']} (confidence: {det['confidence']:.2f})" 
        for det in detections
    ])
    prompt = (
        f"Provide a concise and creative caption for an image that contains the following objects: {detected_objects}. "
    )
    if context_text:
        prompt += f"Additional context: {context_text[:500]}..."
    
    payload = {
        "model": "ollama-model",  # placeholder model name; replace as needed
        "prompt": prompt,
        "stream": False
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
