import requests
import json

def generate_text_description(detections, api_url, pdf_text):
    detected_objects = [
        f"{det['class']} (confidence: {det['confidence']:.2f})"
        for det in detections
    ]
    prompt = (
        "Considering the detected objects and the provided document context, "
        "give a concise description of what the image represents. "
        "Detected objects: " + ", ".join(detected_objects) + ". " +
        "Document context: " + pdf_text[:500] + "..."
    )

    payload = {
        "model": "deepseek-r1:8b",
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