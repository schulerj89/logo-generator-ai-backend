# -*- coding: utf-8 -*-
"""MongoDB service to interact with the database."""
import os
from datetime import datetime
from pymongo import MongoClient

# MongoDB setup
mongo_client = MongoClient(os.getenv("MONGO_URI"))
db = mongo_client.mydatabase

# Ensure collections exist or create them
if "images" not in db.list_collection_names():
    collection = db.create_collection("images")
else:
    collection = db.images

if "prompts" not in db.list_collection_names():
    prompt_collection = db.create_collection("prompts")
else:
    prompt_collection = db.prompts


def get_image_by_prompt(user_prompt):
    """Get image metadata by user prompt from MongoDB."""
    image = collection.find_one({"user_prompt": user_prompt}, {"_id": 0})
    return image

def save_image_metadata(user_prompt, first_prompt, new_prompt, s3_url, filename):
    """Save image metadata to MongoDB."""
    image_metadata = {
        "user_prompt": user_prompt,
        "new_prompt": new_prompt,
        "first_prompt": first_prompt,
        "s3_url": s3_url,
        "filename": filename,
        "created_at": datetime.utcnow()  # Add a created_at field with the current UTC time
    }
    collection.insert_one(image_metadata)

def get_all_images_metadata(page, limit):
    """Get paginated images metadata from MongoDB."""
    # Calculate how many documents to skip based on the current page
    skip = (page - 1) * limit

    # Fetch the paginated images
    images = collection.find({}, {"_id": 0, "user_prompt": 1, "s3_url": 1, "filename": 1}) \
                       .sort("created_at", -1) \
                       .skip(skip) \
                       .limit(limit)

    # Count the total number of images in the collection
    total_images = collection.count_documents({})

    return list(images), total_images

def save_prompt(prompt):
    """Save prompt to MongoDB."""
    prompt_metadata = {
        "prompt": prompt,
        "created_at": datetime.utcnow()  # Add a created_at field with the current UTC time
    }
    prompt_collection.insert_one(prompt_metadata)
