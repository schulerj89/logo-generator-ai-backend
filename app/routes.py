# -*- coding: utf-8 -*-
"""Main routes for the Flask app."""
from io import BytesIO
import logging
from flask import Blueprint, request, jsonify, send_file, make_response, current_app
from .services.openai_service import generate_image_prompt, generate_random_prompts
from .services.s3_service import upload_image_to_s3, get_image_from_s3
from .services.image_service import process_image
from .db.mongo_service import save_image_metadata, get_all_images_metadata, save_prompt, get_image_by_prompt
from .exceptions import InappropriatePromptException


main_routes = Blueprint('main_routes', __name__)

@main_routes.route('/images/<filename>', methods=['GET'])
def serve_image(filename):
    """Serve an image from S3 with Redis caching."""
    try:
        # Access the Redis cache directly
        redis_cache = current_app.cache  # Direct access to Redis client

        # Try to get image data from Redis cache
        cached_image_data = redis_cache.get(filename)
        if cached_image_data is not None:
            return make_response(send_file(BytesIO(cached_image_data), mimetype='image/png'))

        # Fetch image from S3 if not in cache
        image_data = get_image_from_s3(filename)

        # Store image data in Redis cache with a 60-second expiration
        redis_cache.set(filename, image_data, timeout=60)

        return make_response(send_file(BytesIO(image_data), mimetype='image/png'))

    except Exception as e:
        logging.error("Error serving image: %s", str(e))
        return jsonify({"status": "error", "message": str(e)}), 500

@main_routes.route('/generate-image', methods=['POST'])
def generate_image():
    """Generate a new image based on user input."""

    # Access the limiter from current_app and apply to this specific route
    limiter = current_app.limiter
    limit_decorator = limiter.limit("4 per minute")  # Limit to 4 requests per minute

    @limit_decorator
    def limited_generate_image():
        try:
            data = request.get_json()
            user_prompt = data.get('prompt', 'Generate a fantasy football cartoon mascot cowboy')
            user_prompt = ' '.join([word.capitalize() for word in user_prompt.split()])

            save_prompt(user_prompt)

            image = get_image_by_prompt(user_prompt)

            if image:
                return jsonify({"status": "success", "filename": image.get('filename')}), 200

            # Generate prompts and get image from OpenAI
            first_prompt, new_prompt, image_url = generate_image_prompt(user_prompt)

            # Check if the prompt is inappropriate
            if image_url == "Error: Inappropriate Prompt":
                return jsonify({"status": "error", "message": "Inappropriate prompt"}), 400

            # Process the image (resize, transparency)
            image_resized, unique_filename = process_image(image_url)

            # Upload the image to S3
            s3_url = upload_image_to_s3(image_resized, unique_filename)

            # Save metadata to MongoDB
            save_image_metadata(user_prompt, first_prompt, new_prompt, s3_url, unique_filename)

            return jsonify({
                "status": "success",
                "filename": unique_filename
            }), 200
        except InappropriatePromptException:
            return jsonify({"status": "error", "message": "Inappropriate prompt"}), 400
        except Exception as e:
            logging.error("Error generating image: %s", str(e))
            return jsonify({"status": "error", "message": str(e)}), 500

    return limited_generate_image()  # Call the rate-limited function

@main_routes.route('/images', methods=['GET'])
def get_images():
    """Get paginated images metadata."""
    try:
        # Get pagination parameters from the request query string
        page = int(request.args.get('page', 1))  # Default to page 1
        limit = int(request.args.get('limit', 10))  # Default to 10 images per page

        # Get paginated images metadata from MongoDB
        images, total_images = get_all_images_metadata(page, limit)

        total_pages = (total_images + limit - 1) // limit  # Calculate the total number of pages

        return jsonify({
            "status": "success",
            "images": images,
            "page": page,
            "limit": limit,
            "total_pages": total_pages,
            "total_images": total_images
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@main_routes.route('/generate-prompts', methods=['GET'])
def get_random_prompts():
    """Get random prompts from the OpenAI."""
    try:
        # Check if the cache has the prompts
        if current_app.cache.get("random_prompts"):
            random_prompts = current_app.cache.get("random_prompts")
            return jsonify({
                "status": "success",
                "prompts": random_prompts
            }), 200


        # Generate random prompts from OpenAI
        random_prompts = generate_random_prompts()

        # Cache the prompts for 1 minute
        current_app.cache.set("random_prompts", random_prompts, timeout=60)

        return jsonify({
            "status": "success",
            "prompts": random_prompts
        }), 200
    except Exception as e:
        logging.error("Error generating random prompts: %s", str(e))
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
