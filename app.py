import os
import requests
from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
from pymongo import MongoClient
import redis
from openai import OpenAI
from PIL import Image
from io import BytesIO
import uuid  # Import UUID module

# Load OpenAI API key from environment variable
openai_api_key = os.getenv('OPENAI_API_KEY')

# Initialize the OpenAI client
openai_client = OpenAI(api_key=openai_api_key)

# Set up Flask app
app = Flask(__name__)
CORS(app)

# MongoDB setup
mongo_client = MongoClient("mongodb://mongo:27017/")
db = mongo_client.mydatabase

# Redis setup
redis_client = redis.Redis(host='redis', port=6379)

# Directory to save images
IMAGE_DIR = 'images'
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

@app.route('/generate-image', methods=['POST'])
def generate_image():
    """Generate an image with OpenAI, process it, and return the URL as JSON"""
    try:
        data = request.get_json()
        prompt = data.get('prompt', 'Generate a fantasy football cartoon mascot cowboy')
        prompt = prompt + ". Do not include any text only if doing city or state acronyms like NY for New York, LA, etc. Football Type Logo. Always use a white background."

        completion = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
                {"role": "system", "content": "You are an expert at creating prompts for Dall-E. Update the prompt you received so that it is more specific and detailed and used so a user can create a fantasy football logo. Make sure to always use a white background."},
                {"role": "user", "content": prompt}
            ]
        )

        first_prompt = completion.choices[0].message.content

        completion_checker = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
                {"role": "system", "content": "You are an expert at keeping prompts concise and to the point for LLMs. Update the prompt you received so that it's simple and to the point. Please always ensure a white background is used and no text is included."},
                {"role": "user", "content": first_prompt}
            ]
        )

        new_prompt = completion_checker.choices[0].message.content

        # Generate image with OpenAI API
        images = openai_client.images.generate(
            model="dall-e-3",
            prompt=new_prompt,
            n=1,
            size="1024x1024"
        )

        # Extract the URL from the response
        image_url = images.data[0].url

        # Download the image from the URL
        response = requests.get(image_url)
        image = Image.open(BytesIO(response.content))

        # Convert the image to RGBA (support transparency)
        image = image.convert("RGBA")

        # Get pixel data
        datas = image.getdata()

        # Create a new image data list where white pixels will be replaced with transparency
        new_data = []
        for item in datas:
            # Change all white (also shades of whites) to transparent
            if item[0] > 200 and item[1] > 200 and item[2] > 200:  # Check if the pixel is white
                new_data.append((255, 255, 255, 0))  # Change to transparent
            else:
                new_data.append(item)  # Keep original pixel

        # Update image data with transparency
        image.putdata(new_data)

        # Resize the image to 256x256
        image_resized = image.resize((256, 256))

        # Generate a unique filename using UUID
        unique_filename = f"{uuid.uuid4()}.png"
        image_path = os.path.join(IMAGE_DIR, unique_filename)

        # Save the resized image with transparency using the unique filename
        image_resized.save(image_path, "PNG")

        # Return the URL of the saved image
        image_api_url = f"http://localhost:5000/images/{unique_filename}"
        return jsonify({
            "status": "success",
            "message": "Image generated and processed successfully.",
            "image_url": image_api_url,
            "prompt": new_prompt,
            "original_prompt": first_prompt
        }), 200

    except Exception as e:
        # Handle any errors that occur
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# Serve the images from the local directory
@app.route('/images/<filename>', methods=['GET'])
def serve_image(filename):
    """Serve images from the local directory"""
    try:
        return send_from_directory(IMAGE_DIR, filename)
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
