import cv2
import numpy as np
import pytesseract
import os
from pdf2image import convert_from_path
from PIL import Image

# ✅ Set Tesseract OCR Path for macOS (Update path if needed)
pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"  # For Apple Silicon (M1/M2)
# If using Intel Mac, change to: "/usr/local/bin/tesseract"

def load_image(input_path, dpi=300):
    """Load an image or convert PDF to an image."""
    if input_path.lower().endswith(".pdf"):
        print("📄 Converting PDF to image...")
        images = convert_from_path(input_path, dpi=dpi)
        return np.array(images[0])  # Convert first page to NumPy array
    else:
        print("🖼️ Loading image file...")
        return cv2.imread(input_path)

def preprocess_image(image):
    """Convert to grayscale and apply edge detection."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 50, 150)  # Edge detection
    return edged

def extract_scale_text(image):
    """Extract scale from blueprint using OCR."""
    print("🔍 Extracting scale information...")
    text = pytesseract.image_to_string(image)

    scale_factor = 1.0  # Default scale
    for line in text.split("\n"):
        if "scale" in line.lower():
            parts = line.split(":")
            if len(parts) == 2 and parts[1].strip().replace(".", "").isdigit():
                scale_factor = float(parts[1].strip())
                break

    print(f"📏 Detected Scale: 1:{scale_factor}")
    return scale_factor

def calculate_area(image, scale=1.0):
    """Detect contours and estimate square area."""
    contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    total_area = sum(cv2.contourArea(contour) for contour in contours)

    real_area = total_area * (scale ** 2)  # Adjust area based on scale
    return real_area

def cal_blueprint(input_path):
    """Main function to process blueprint and estimate area."""
    if not os.path.exists(input_path):
        print("❌ Error: File not found!")
        return

    # Load image from PDF or Image
    image = load_image(input_path)

    # Convert to PIL Image for OCR
    pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    # Extract scale from the blueprint
    scale = extract_scale_text(pil_image)

    # Process image for contour detection
    processed_image = preprocess_image(image)

    # Calculate square area
    area = calculate_area(processed_image, scale)
    print(f"✅ Estimated Square Area: {area:.2f} sq units")

    return {"estimated_area": round(area, 2)}
