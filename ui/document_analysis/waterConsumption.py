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

def extract_water_certification_from_text(text):
    """
    Uses LM Studio to extract water supply certification details from the provided text.

    The prompt instructs the model to extract the following details:
      - Total Monthly Water Consumption (numeric value, in Liters)
      - Primary Water Source (with percentage if available)
      - Secondary Water Source (with percentage if available)
      - Average pH Level
      - Monthly Water Cost (numeric value)
      - Usage Breakdown percentages for:
            • Manufacturing Processes
            • Cooling Systems
            • Sanitation
      - Water Quality details:
            • pH Level
            • Turbidity
            • Contaminants
      - Testing Authority
      - Test Date (or date of latest water quality test)

    The response should be a well-formatted JSON object with the following structure:
    {
        "Total_monthly_water_consumption": <number or null>,
        "primary_water_source": <string or null>,
        "secondary_water_source": <string or null>,
        "average_ph_level": <number or null>,
        "monthly_water_cost": <number or null>,
        "usage_breakdown": {
            "manufacturing_processes": <number or null>,
            "cooling_systems": <number or null>,
            "sanitation": <number or null>
        },
        "water_quality": {
            "ph_level": <number or null>,
            "turbidity": <string or null>,
            "contaminants": <string or null>
        },
        "testing_authority": <string or null>,
        "test_date": <string or null>
    }

    Do not include any additional text or markdown code blocks in the response.

    Args:
        text (str): The full text extracted from the document.

    Returns:
        dict: A JSON object containing the extracted water certification details or an error message.
    """
    prompt = f"""
Please analyze the following water supply certification and usage report. The report may contain explicit fields or require deducing the following details:

- Total Monthly Water Consumption (e.g., "1,50,000 Liters") – extract the numeric value and return it as Total_monthly_water_consumption.
- Primary Water Source (e.g., "Dedicated Borewell (70%)") – extract as primary_water_source.
- Secondary Water Source (e.g., "Municipal Water Supply (30%)") – extract as secondary_water_source.
- Average pH Level (e.g., "7.2") – extract as average_ph_level.
- Monthly Water Cost (e.g., "INR 75,000") – extract the numeric value as monthly_water_cost.
- Usage Breakdown – extract percentages for:
    - Manufacturing Processes (e.g., 80) as manufacturing_processes.
    - Cooling Systems (e.g., 15) as cooling_systems.
    - Sanitation (e.g., 5) as sanitation.
- Water Quality details – extract:
    - pH Level (e.g., "7.2") as ph_level.
    - Turbidity (e.g., "Low") as turbidity.
    - Contaminants (e.g., "Within permissible limits") as contaminants.
- Testing Authority (e.g., "National Water Quality Board") as testing_authority.
- Test Date (e.g., "Conducted on March 5, 2025") as test_date.

Return the extracted information as a well-formatted JSON object with the following structure:
{{
    "Total_monthly_water_consumption": <number or null>,
    "primary_water_source": <string or null>,
    "secondary_water_source": <string or null>,
    "average_ph_level": <number or null>,
    "monthly_water_cost": <number or null>,
    "usage_breakdown": {{
        "manufacturing_processes": <number or null>,
        "cooling_systems": <number or null>,
        "sanitation": <number or null>
    }},
    "water_quality": {{
        "ph_level": <number or null>,
        "turbidity": <string or null>,
        "contaminants": <string or null>
    }},
    "testing_authority": <string or null>,
    "test_date": <string or null>
}}

Do not include any additional text or markdown code blocks in the response.

TEXT:
{text}
    """

    payload = {
        "model": "amethyst-13b-mistral",  # Ensure this model is available in LM Studio
        "messages": [
            {"role": "system", "content": "Extract the water supply certification details from the document."},
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

def extract_water_certification_from_pdf(pdf_path):
    """
    Extracts text from a PDF document and uses LM Studio to determine the water supply certification details.

    Args:
        pdf_path (str): The path to the PDF file.

    Returns:
        dict: A JSON object containing the water certification details or an error message.
    """
    text = extract_text_from_pdf(pdf_path)
    if not text:
        print("No text extracted from the PDF!")
        return {"error": "No text could be extracted from the PDF"}
    print("Extracted text (first 500 characters):")
    print(text[:500])
    result = extract_water_certification_from_text(text)
    return result
