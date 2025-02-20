import os
import argparse
from PIL import Image
from utils.pdf_utils import extract_images_from_pdf, extract_text_from_pdf
from utils.image_utils import generate_image_caption
from utils.ollama_utils import load_ollama_model

def process_pdf(pdf_path, api_url):
    images = extract_images_from_pdf(pdf_path)
    pdf_text = extract_text_from_pdf(pdf_path)

    if not images:
        return

    for image in images:
        try:
            description = generate_image_caption(image, api_url, context_text=pdf_text)
            print(description, end='')  # Remove newline
        except Exception:
            pass  # Silently handle errors

def process_image(image_path, api_url):
    try:
        image = Image.open(image_path).convert("RGB")
        description = generate_image_caption(image, api_url)
        print(description, end='')  # Remove newline
    except Exception:
        pass  # Silently handle errors

def main():
    parser = argparse.ArgumentParser(
        description="Process an input file (PDF or image) and generate descriptions using the Ollama model."
    )
    parser.add_argument("input_file", help="Path to the input file (PDF or image)")
    parser.add_argument(
        "--api_url", 
        default="http://localhost:11434/api/generate",
        help="Ollama model API URL"
    )
    args = parser.parse_args()

    # Silently create outputs directory
    os.makedirs('outputs', exist_ok=True)
    
    # Load model without output
    load_ollama_model(silent=True)  # You'll need to modify ollama_utils.py to accept this parameter

    input_file = args.input_file
    ext = os.path.splitext(input_file)[1].lower()
    if ext == ".pdf":
        process_pdf(input_file, args.api_url)
    elif ext in [".jpg", ".jpeg", ".png", ".bmp", ".tiff"]:
        process_image(input_file, args.api_url)

if __name__ == "__main__":
    main()