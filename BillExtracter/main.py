import cv2
import pytesseract
import layoutparser as lp

# Load and preprocess the image
image_path = "invoice.png"

# Convert to grayscale and threshold
img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

# Save the processed image
cv2.imwrite("preprocessed_invoice.png", img)

# Run Tesseract OCR
custom_config = r'--oem 3 --psm 6'  # OCR Engine Mode (oem) & Page Segmentation Mode (psm)
extracted_text = pytesseract.image_to_string(img, config=custom_config)

print("Extracted Text:\n", extracted_text)
