import cv2
import numpy as np
import pytesseract
import os
from pdf2image import convert_from_path
from PIL import Image

# Set the path to Tesseract OCR (Modify if needed)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

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
            if len(parts) == 2 and parts[1].strip().isdigit():
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

def calculate_facility_area(input_path, dpi=300):
    """
    Process a blueprint (PDF or image) and return the calculated square area.
    
    Args:
        input_path (str): Path to the PDF or image file
        dpi (int): DPI for PDF conversion (default: 300)
    
    Returns:
        float: Calculated square area
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError("❌ Error: File not found!")
    
    # Load image from PDF or Image
    image = load_image(input_path, dpi)
    
    # Convert to PIL Image for OCR
    pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    
    # Extract scale from the blueprint
    scale = extract_scale_text(pil_image)
    
    # Process image for contour detection
    processed_image = preprocess_image(image)
    
    # Calculate and return square area
    return calculate_area(processed_image, scale)

def main(input_path):
    """Main function to process blueprint and estimate area."""
    try:
        area = calculate_facility_area(input_path)
        print(f"✅ Estimated Square Area: {area:.2f} sq units")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    input_path = "image.png"  # Replace with your file (PDF or Image)
    main(input_path)
