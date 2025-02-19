from pdf2image import convert_from_path
from pdfminer.high_level import extract_text

def extract_images_from_pdf(pdf_path):
    images = convert_from_path(pdf_path)
    return images

def extract_text_from_pdf(pdf_path):
    try:
        text = extract_text(pdf_path)
        return text.strip()
    except Exception as e:
        return f"Error extracting text: {str(e)}"
