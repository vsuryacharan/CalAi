from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import base64
import os

app = Flask(__name__)

# Gemini API key setup
genai.configure(api_key='AIzaSyAQsYO-KF8txATW2oY-OVGXlkrmONoJbmk')

def prep_image(image_path):
    # Upload the file and print a confirmation.
    sample_file = genai.upload_file(path=image_path, display_name="Diagram")
    print(f"Uploaded file '{sample_file.display_name}' as: {sample_file.uri}")
    return sample_file

def extract_text_from_image(image_path, prompt):
    # Choose a Gemini model.
    model = genai.GenerativeModel(model_name="gemini-1.5-pro")
    # Prompt the model with text and the previously uploaded image.
    response = model.generate_content([image_path, prompt])
    
    # Log the response for debugging
    print(f"Response from Gemini: {response.text}")

    return response.text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/solve-equation', methods=['POST'])
def solve_equation():
    data = request.json
    image_data = data['image']  # Base64 encoded image from canvas
    
    # Decode the base64 image data to save it temporarily
    try:
        image_data = image_data.split(",")[1]  # Get the base64 part
        img_bytes = base64.b64decode(image_data)
        image_path = 'temp_image.png'  # Temporary path to save the image

        # Save the image temporarily
        with open(image_path, 'wb') as f:
            f.write(img_bytes)

        # Create a prompt for the Gemini model
        prompt = "Extract the text in the image verbatim."

        # Upload the image and extract text using the provided functions
        prep_image(image_path)
        text = extract_text_from_image(image_path, prompt)

        # Clean up the temporary image file
        #os.remove(image_path)  # Remove the image after use

        return jsonify({"solution": text})
    
    except Exception as e:
        print(f"Error processing image: {e}")
        return jsonify({"solution": "Error processing the image."})

if __name__ == '__main__':
    app.run(debug=True)
