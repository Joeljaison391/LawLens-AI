import os
import sys
import json
import requests
import PyPDF2
from pdf2image import convert_from_path
import pytesseract

# Ensure the root directory (SoulSync) is in sys.path if needed
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

# LM Studio API URL (Make sure LM Studio is running)
LM_STUDIO_URL = "http://localhost:1234/v1/chat/completions"


def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file using PyPDF2 and pytesseract for OCR.

    Args:
        pdf_path (str): The path to the PDF file.

    Returns:
        str: The extracted text.
    """
    text = ""
    try:
        with open(pdf_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

        # If no text was extracted, use OCR
        if not text.strip():
            images = convert_from_path(pdf_path)
            for image in images:
                text += pytesseract.image_to_string(image) + "\n"
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text.strip()


def extract_employee_count_from_text(text):
    """
    Uses LM Studio to extract the total number of employees from the provided text.

    The prompt instructs the model to look for an explicit field like "Total Number of Employees"
    or deduce the count based on contextual payroll details.

    Args:
        text (str): The full text extracted from the document.

    Returns:
        dict: A JSON object with the key "employee_count" or an error message.
    """
    prompt = f"""
Please analyze the following company payroll and registration report. The report may contain an explicit field such as "Total Number of Employees" or require deducing the total employee count from the context (for example, by interpreting payroll summaries or employee listings).

Extract and return the total number of employees in the following JSON format:
{{
    "employee_count": <number or null>
}}

TEXT:
{text}
    """

    payload = {
        "model": "amethyst-13b-mistral",  # Ensure this model is available in LM Studio
        "messages": [
            {"role": "system", "content": "Extract the total number of employees from the document."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2,
        "max_tokens": 256,
        "stream": False
    }

    try:
        response = requests.post(LM_STUDIO_URL, json=payload, headers={"Content-Type": "application/json"})
        response.raise_for_status()
        response_data = response.json()
        structured_json = response_data.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
        print("LM Studio raw response:", structured_json)
        if not structured_json:
            print("LM Studio returned an empty response!")
            return {"error": "No valid JSON response from LM Studio"}
        return json.loads(structured_json)
    except json.JSONDecodeError as e:
        print(f"JSONDecodeError: {e}")
        return {"error": "Invalid JSON response from LM Studio"}
    except requests.RequestException as e:
        print(f"RequestException: {e}")
        return {"error": "Failed to connect to LM Studio"}


def extract_employee_count_from_pdf(pdf_path):
    """
    Extracts text from a PDF document and uses LM Studio to determine the total number of employees.

    Args:
        pdf_path (str): The path to the PDF file.

    Returns:
        dict: A JSON object containing the employee count or an error message.
    """
    text = extract_text_from_pdf(pdf_path)
    if not text:
        print("No text extracted from the PDF!")
        return {"error": "No text could be extracted from the PDF"}
    print("Extracted text (first 500 characters):")
    print(text[:500])
    result = extract_employee_count_from_text(text)
    return result