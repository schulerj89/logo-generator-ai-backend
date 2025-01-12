# -*- coding: utf-8 -*-
"""Image processing service."""
import uuid
from io import BytesIO
import requests
from PIL import Image

def process_image(image_url):
    """Process the image by converting and resizing it."""
    # Download the image from the URL
    response = requests.get(image_url)
    image = Image.open(BytesIO(response.content))

    # Convert and resize image
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

    # Generate unique filename
    unique_filename = f"{uuid.uuid4()}.png"

    return image_resized, unique_filename
    
