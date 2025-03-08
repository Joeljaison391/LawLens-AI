import cv2
import pytesseract
import layoutparser as lp
import requests
import json
import io
import os
import sys
from PIL import Image

# Ensure the root directory (SoulSync) is in sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

# LM Studio API URL (Make sure LM Studio is running)
LM_STUDIO_URL = "http://localhost:1234/v1/chat/completions"

simple_json_extract = """
Extract structured data from the following document and return it in valid JSON format. The JSON should only include these specific fields:
- name: Name of the facility/building
- square_feet: Total square footage of the facility
- number_of_employees: Number of employees working in the facility
- power_consumption: Power consumption details
- water_source: Source of water supply
- waste_disposal: Waste management and disposal methods

TEXT:
{text}

Return **only** the extracted information as a well-formatted JSON object with the above fields. If a field's information is not found in the text, use null as the value. Do not include any additional text or markdown code blocks in the response.
"""


def extract_text_from_image(image_path):
    """Extracts text from an image using OpenCV, Tesseract OCR, and LayoutParser."""
    print(f"🔍 Processing image: {image_path}")

    # Load image and preprocess
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    cv2.imwrite("preprocessed_invoice.png", img)  # Save processed image

    # Perform OCR
    custom_config = r'--oem 3 --psm 6'
    extracted_text = pytesseract.image_to_string(img, config=custom_config)

    print(f"✅ Extracted Text: {extracted_text[:10000]}...")  # Preview first 100 chars
    return extracted_text.strip()


def analyze_text_with_lm_studio(text):
    """
    Uses LM Studio to analyze extracted text and convert it into structured JSON.

    Args:
        text (str): The extracted text from a document.

    Returns:
        dict: The extracted structured information in JSON format.
    """
    print("🔍 Sending text to LM Studio API...")

    # Define system prompt
    system_prompt = """Extract structured data from the following document and return it in valid JSON format. 
The JSON should only include these specific fields:

- name: Name of the facility/building
- square_feet: Total square footage of the facility
- number_of_employees: Number of employees working in the facility
- power_consumption: Power consumption details
- water_source: Source of water supply
- waste_disposal: Waste management and disposal methods

TEXT:
{text}

Return **only** the extracted information as a well-formatted JSON object with the above fields. 
If a field's information is not found in the text, use null as the value. 
Do not include any additional text or markdown code blocks in the response.

"""

    # Format the prompt with actual text
    prompt = system_prompt.format(text=text)

    # Construct payload for LM Studio API
    payload = {
        "model": "amethyst-13b-mistral",  # Ensure this model is available in LM Studio
        "messages": [
            {"role": "system", "content": "Extract structured data from this text and return valid JSON"},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2,  # Lower temperature for better consistency
        "max_tokens": 1024,  # Set max tokens limit
        "stream": False
    }

    try:
        # Send request to LM Studio
        response = requests.post(LM_STUDIO_URL, json=payload, headers={"Content-Type": "application/json"})
        response.raise_for_status()

        # Parse response JSON
        response_data = response.json()
        structured_json = response_data.get("choices", [{}])[0].get("message", {}).get("content", "").strip()

        # Debugging logs
        print(f"🌐 API Response Status: {response.status_code}")
        print(f"🔍 Raw LM Studio Response:\n{structured_json}")

        # Validate JSON response
        if not structured_json:
            print("⚠️ LM Studio returned an empty response!")
            return {"error": "No valid JSON response from LM Studio"}

        return json.loads(structured_json)  # Convert string to JSON object

    except json.JSONDecodeError as e:
        print(f"⚠️ JSONDecodeError: {e}")
        return {"error": "Invalid JSON response from LM Studio"}
    except requests.RequestException as e:
        print(f"⚠️ RequestException: {e}")
        return {"error": "Failed to connect to LM Studio"}

def analyze_invoice(image_path):
    """
    Analyzes an invoice image and returns structured JSON data.

    Args:
        image_path (str): Path to the invoice image

    Returns:
        dict: Structured JSON data extracted from the invoice
    """
    print("🚀 Starting invoice analysis...")
    extracted_text = extract_text_from_image(image_path)

    if not extracted_text:
        print("⚠️ No text extracted from image!")
        return {"error": "No text could be extracted from the image"}

    print("📨 Sending extracted text to LM Studio for analysis...")
    structured_data = analyze_text_with_lm_studio(extracted_text)
    print("✅ Analysis complete. Structured Data:", structured_data)
    return structured_data
