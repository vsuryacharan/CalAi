import openai
import pytesseract
import os
from dotenv import load_dotenv
from PIL import Image

# Load API keys from .env
load_dotenv()
openai.api_key = os.getenv("Osk-5xbYmQFB-siwYfOiGoDB1jNRmom_C3VsAxUqfv-t3YT3BlbkFJf3_xU1N-wI5wdawDnQbMvfvExpfnAxGr_S_-N0y4cA")

# Convert image to text using OCR and solve using OpenAI
def analyze_image(img: Image):
    # Convert image to text (OCR) using pytesseract
    text = pytesseract.image_to_string(img)

    # Check if any text is extracted
    if not text.strip():
        return "Could not detect any text in the image."

    # Use OpenAI to solve the equation
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Solve this mathematical equation: {text}",
            max_tokens=100
        )
        solution = response['choices'][0]['text'].strip()
        return solution
    except Exception as e:
        return f"Error in AI processing: {str(e)}"
