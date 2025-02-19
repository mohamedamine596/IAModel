from pdf2image import convert_from_path
from pdfminer.high_level import extract_text
from pdf2image.exceptions import PDFPageCountError

def extract_images_from_pdf(pdf_path):
    """
    Extracts all pages from a PDF as PIL Image objects.
    Requires 'poppler' installed for pdf2image.
    """
    try:
        images = convert_from_path(pdf_path)
        return images
    except Exception as e:
        print(f"Error extracting images from PDF: {e}")
        return []

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file using pdfminer.
    """
    try:
        text = extract_text(pdf_path)
        return text if text else ""
    except Exception as e:
        print(f"Error extracting text: {e}")
        return ""
