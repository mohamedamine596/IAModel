import requests
import json

def generate_description(detections, api_url, pdf_text):
    detected_objects = [
        f"{det['class']} (confidence: {det['confidence']:.2f})"
        for det in detections
    ]
    prompt = (
        "Based on the detected objects and the accompanying document text, "
        "provide a concise yet informative description of what the image represents. "
        f"Detected: {', '.join(detected_objects)}. "
        f"Document text: {pdf_text}"
    )

    payload = {
        "model": "deepseek-r1:8b",  # Optimized model selection
        "prompt": prompt,
        "stream": False
    }

    print("Payload being sent to Ollama:", json.dumps(payload, indent=2))

    try:
        response = requests.post(api_url, json=payload)
        response.raise_for_status()

        print("🔍 Raw Response from Ollama API:", response.text)

        result = response.json()

        if "response" in result:
            return result["response"]
        else:
            return f"Unexpected response format: {result}"

    except json.JSONDecodeError:
        return "Error decoding JSON from Ollama API"
    except requests.exceptions.RequestException as e:
        return f"Error generating description: {str(e)}"