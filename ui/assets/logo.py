import streamlit as st
from PIL import Image
import os

def get_logo():
    """
    Returns the logo image resized to be smaller.
    Looks for image.png in several possible locations.
    """
    # List of possible image locations
    possible_paths = [
        "image.png",                       # Root directory
        "assets/image.png",                # assets folder
        "SoulSync/ui/assets/image.png",    # UI assets folder
        "../image.png",                    # One level up
        "../../image.png",                 # Two levels up
    ]
    
    # Try to find the image file
    image_path = None
    for path in possible_paths:
        if os.path.exists(path):
            image_path = path
            break
    
    # If image not found, return None
    if image_path is None:
        return None
        
    # Open and resize the image
    try:
        image = Image.open(image_path)
        # Resize the image to be smaller (80px width while preserving aspect ratio)
        width, height = image.size
        new_width = 80
        new_height = int(height * (new_width / width))
        resized_image = image.resize((new_width, new_height))
        return resized_image
    except Exception as e:
        print(f"Error loading logo: {e}")
        return None

# Keep the base64 function for backward compatibility
def get_logo_base64():
    return """
    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
    """ 