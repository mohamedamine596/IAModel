import os
import argparse
from PIL import Image
from utils.pdf_utils import extract_images_from_pdf, extract_text_from_pdf
from utils.image_utils import generate_image_caption
from utils.ollama_utils import load_ollama_model

def process_pdf(pdf_path, api_url):
    print("Extracting images from PDF...")
    images = extract_images_from_pdf(pdf_path)
    print("Extracting text from PDF...")
    pdf_text = extract_text_from_pdf(pdf_path)

    if not images:
        print("No images found in the PDF.")
        return

    for i, image in enumerate(images, 1):
        print(f"\nProcessing image {i} of {len(images)}")
        try:
            print("Generating image description using Ollama model...")
            description = generate_image_caption(image, api_url, context_text=pdf_text)

            print("Saving results...")
            output_image_path = f'outputs/pdf_image_{i}.png'
            image.save(output_image_path)
            with open(f'outputs/pdf_image_{i}_description.txt', 'w') as f:
                f.write("Image Description:\n" + description)

            print(f"Image {i} processed successfully.")
            print(f"Image Description: {description}")
        except Exception as e:
            print(f"Error processing image {i}: {str(e)}")
            continue

def process_image(image_path, api_url):
    print("Opening image...")
    try:
        image = Image.open(image_path).convert("RGB")
    except Exception as e:
        print(f"Error opening image: {str(e)}")
        return

    try:
        print("Generating image description using Ollama model...")
        description = generate_image_caption(image, api_url)

        print("Saving results...")
        output_image_path = 'outputs/image.png'
        image.save(output_image_path)
        with open('outputs/image_description.txt', 'w') as f:
            f.write("Image Description:\n" + description)

        print("Image processed successfully.")
        print(f"Image Description: {description}")
    except Exception as e:
        print(f"Error processing image: {str(e)}")

def main():
    parser = argparse.ArgumentParser(
        description="Process an input file (PDF or image) and generate descriptions using the Ollama model."
    )
    parser.add_argument("input_file", help="Path to the input file (PDF or image)")
    parser.add_argument(
        "--api_url", 
        default="http://localhost:11434/api/generate",  # Corrected endpoint
        help="Ollama model API URL (default: http://localhost:11434/api/generate)"
    )
    args = parser.parse_args()

    os.makedirs('outputs', exist_ok=True)

    print("Loading Ollama model...")
    load_ollama_model()  # Ensures Ollama is installed, model is pulled, and server is running.

    input_file = args.input_file
    ext = os.path.splitext(input_file)[1].lower()
    if ext == ".pdf":
        process_pdf(input_file, args.api_url)
    elif ext in [".jpg", ".jpeg", ".png", ".bmp", ".tiff"]:
        process_image(input_file, args.api_url)
    else:
        print("Unsupported file format. Please provide a PDF or an image file.")

if __name__ == "__main__":
    main()