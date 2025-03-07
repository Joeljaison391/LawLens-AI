import fitz  # PyMuPDF for PDF processing
import pytesseract  # OCR for scanned PDFs
from PIL import Image
import ollama
import json
import io
import re
from SoulSync.processing.bill_extractor.prompts import simple_json_extract

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF using PyMuPDF and OCR for scanned documents."""
    doc = fitz.open(pdf_path)
    extracted_text = ""

    for page in doc:
        text = page.get_text("text")
        if text.strip():
            extracted_text += text + "\n"
        else:
            # Perform OCR if no text is found (for scanned images)
            pix = page.get_pixmap()
            img = Image.open(io.BytesIO(pix.tobytes("png")))
            ocr_text = pytesseract.image_to_string(img)
            extracted_text += ocr_text + "\n"
    
    return extracted_text.strip()

def analyze_text_with_ollama(text):
    """Uses Ollama AI to analyze extracted text and convert it into structured JSON."""
    prompt = simple_json_extract.format(text=text)

    response = ollama.chat(
        model="llama3.2:latest",  # Use 'llama3' or 'mixtral' based on your setup
        messages=[{"role": "user", "content": prompt}]
    )

    structured_json = response.get("message", {}).get("content", "").strip()

    # 🔍 Debugging: Print raw response to check if it's empty
    print("🔍 Raw Ollama Response:", structured_json)

    if not structured_json:
        print("⚠️ Ollama returned an empty response!")
        return {"error": "No valid JSON response from Ollama"}

    try:
        return json.loads(structured_json)  # Safely parse JSON
    except json.JSONDecodeError as e:
        print(f"⚠️ JSONDecodeError: {e}")
        return {"error": "Invalid JSON response from Ollama"}

def convert_pdf_to_json(pdf_path, json_path):
    """Extracts text from a PDF, analyzes it using Ollama, and saves structured JSON."""
    extracted_text = extract_text_from_pdf(pdf_path)
    
    if not extracted_text:
        print("⚠️ No text extracted from PDF!")
        return

    structured_data = analyze_text_with_ollama(extracted_text)

    # Save to JSON file
    with open(json_path, "w", encoding="utf-8") as json_file:
        json.dump(structured_data, json_file, indent=4, ensure_ascii=False)
    
    print(f"✅ JSON saved to {json_path}")

# Example usage
pdf_file = "./pdf_outputs/fire_extinguisher_invoice.pdf"  # Replace with your generated invoice file
json_file = "invoice_output.json"  # Output JSON file
convert_pdf_to_json(pdf_file, json_file)
