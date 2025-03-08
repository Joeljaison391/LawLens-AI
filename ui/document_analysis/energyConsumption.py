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
    Extracts text from a PDF file using PyPDF2 and pytesseract for OCR if necessary.

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

        # If no text was extracted using PyPDF2, use OCR via pdf2image and pytesseract.
        if not text.strip():
            images = convert_from_path(pdf_path)
            for image in images:
                text += pytesseract.image_to_string(image) + "\n"
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text.strip()

def extract_power_consumption_from_text(text):
    """
    Uses LM Studio to extract the power consumption report from the provided text.

    The prompt instructs the model to search for overall energy details and machine-specific power data,
    and to return the extracted information in a well-formatted JSON structure as follows:

    {
        "Total_consumption": <number or null>,   // e.g., 6000
        "details_of_machine": [
            {
                "machine_id": <string or null>,
                "machine_name": <string or null>,
                "power_kw": <number or null>,
                "pollution_rate": <string or null>,
                "manufacturer": <string or null>,
                "purchase_date": <string or null>
            },
            ...
        ]
    }

    If a field's information is not found in the text, use null as the value.

    Args:
        text (str): The full text extracted from the document.

    Returns:
        dict: A JSON object containing the extracted power consumption data or an error message.
    """
    prompt = f"""
Please analyze the following energy consumption and machinery report. The report may contain explicit fields or require deducing the following details:

- Total Energy Consumption (e.g., "120,000 kWh (Monthly)") – extract the numeric value and return it as Total_consumption.
- Machinery details: For each machine, extract the following:
    - machine_id
    - machine_name
    - power_kw (in kW)
    - pollution_rate (e.g., Low, Moderate, High)
    - manufacturer
    - purchase_date

Return the extracted information as a well-formatted JSON object with the following structure:
{{
    "Total_consumption": <number or null>,
    "details_of_machine": [
        {{
            "machine_id": <string or null>,
            "machine_name": <string or null>,
            "power_kw": <number or null>,
            "pollution_rate": <string or null>,
            "manufacturer": <string or null>,
            "purchase_date": <string or null>
        }},
        ...
    ]
}}

Do not include any additional text or markdown code blocks in the response.

TEXT:
{text}
    """

    payload = {
        "model": "amethyst-13b-mistral",  # Ensure this model is available in LM Studio
        "messages": [
            {"role": "system", "content": "Extract the power consumption report from the document."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2,
        "max_tokens": 512,
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

def extract_power_consumption_from_pdf(pdf_path):
    """
    Extracts text from a PDF document and uses LM Studio to determine the overall power consumption report.

    Args:
        pdf_path (str): The path to the PDF file.

    Returns:
        dict: A JSON object containing the power consumption report or an error message.
    """
    text = extract_text_from_pdf(pdf_path)
    if not text:
        print("No text extracted from the PDF!")
        return {"error": "No text could be extracted from the PDF"}
    print("Extracted text (first 500 characters):")
    print(text[:500])
    result = extract_power_consumption_from_text(text)
    return result
