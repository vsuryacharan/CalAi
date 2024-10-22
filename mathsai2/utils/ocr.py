import base64
import os
from io import BytesIO
from PIL import Image

# Convert handwriting to text with preprocessing and save to a file
def convert_handwriting_to_text(image_data):
    # Decode the base64 image data
    image_data = image_data.split(",")[1]
    img_bytes = base64.b64decode(image_data)
    img = Image.open(BytesIO(img_bytes))

    # Save the image to a temporary file
    image_path = 'temp_image.png'
    img.save(image_path)

    return image_path  # Return the path for uploading to Gemini
