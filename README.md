# Flask Image Generator API

This project provides a backend API built using **Flask** that integrates with **OpenAI's DALL-E** model to generate custom images based on user input. The API processes the generated image, makes the white background transparent, resizes it, and serves it through a unique URL. It supports saving image metadata in **MongoDB** and integrates with **Amazon S3** for image storage. Optionally, **Redis** can be used for caching.

## Features
- Generates images based on prompts using OpenAI's DALL-E API.
- Makes the background transparent and resizes images to 256x256 pixels.
- Stores and serves images through **Amazon S3**.
- Saves image metadata (prompt, URL, etc.) in **MongoDB**.
- Provides random prompt generation.
- Offers paginated retrieval of image metadata.
- CORS enabled for cross-origin requests.

## Technologies
- **Flask**: Python web framework.
- **OpenAI API**: Used for generating images and prompts.
- **Pillow (PIL)**: Python Imaging Library for image manipulation.
- **UUID**: Ensures image filenames are unique.
- **MongoDB**: Stores image metadata.
- **Amazon S3**: Stores processed images and serves them via a URL.
- **Redis**: Optional caching system for performance improvement.

## Endpoints

### `POST /generate-image`
Generates an image based on the provided prompt, processes it, uploads it to S3, and returns the filename of the image.

- **URL**: `http://localhost:5000/generate-image`
- **Method**: POST
- **Request Body** (JSON):
  ```json
  {
    "prompt": "Generate a futuristic football team logo"
  }
  ```
- **Response** (JSON):
  ```json
  {
    "status": "success",
    "filename": "unique_image_id.png"
  }
  ```
  - On error, the response will include an appropriate error message and status.

### `GET /images/<filename>`
Serves an image file from **Amazon S3** by filename.

- **URL**: `http://localhost:5000/images/{uuid}.png`
- **Method**: GET
- **Response**: Returns the image file (PNG) from S3.

### `GET /images`
Returns paginated metadata for all images generated, including prompts and URLs.

- **URL**: `http://localhost:5000/images`
- **Method**: GET
- **Query Parameters**:
  - `page`: Page number (default: 1)
  - `limit`: Number of images per page (default: 10)
- **Response** (JSON):
  ```json
  {
    "status": "success",
    "images": [
      {
        "prompt": "Fantasy Football Logo",
        "first_prompt": "Fantasy Football Logo",
        "new_prompt": "Fantasy Football Logo Updated",
        "image_url": "https://your-s3-bucket.s3.amazonaws.com/images/unique_image_id.png",
        "filename": "unique_image_id.png"
      },
      ...
    ],
    "page": 1,
    "limit": 10,
    "total_pages": 5,
    "total_images": 50
  }
  ```

### `GET /generate-prompts`
Generates and returns random image prompts using **OpenAI's** API.

- **URL**: `http://localhost:5000/generate-prompts`
- **Method**: GET
- **Response** (JSON):
  ```json
  {
    "status": "success",
    "prompts": [
      "A futuristic football team logo",
      "A fantasy dragon mascot",
      "A cyberpunk warrior",
      ...
    ]
  }
  ```

## Setup and Installation

### Prerequisites
- Python 3.x
- Flask
- MongoDB
- AWS Account for S3 (optional)
- Redis (optional)

### Installation Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-repo/flask-image-generator.git
   cd flask-image-generator
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   Create a `.env` file in the root directory and add your environment-specific keys:
   ```bash
   OPENAI_API_KEY=your-openai-api-key
   AWS_ACCESS_KEY_ID=your-aws-access-key
   AWS_SECRET_ACCESS_KEY=your-aws-secret-key
   AWS_REGION=your-aws-region
   S3_BUCKET_NAME=your-s3-bucket-name
   ```

5. **Run the application**:
   ```bash
   flask run
   ```

6. The API should now be available at `http://localhost:5000`.

## Image Processing
- The generated images are resized to 256x256 pixels and have transparent backgrounds.
- Images are uploaded to **Amazon S3** and can be accessed via the returned filenames.
- Metadata, including the prompts and generated URLs, is stored in **MongoDB** for future reference.

## Error Handling
- The API handles invalid JSON input by returning a `400` status with an appropriate error message.
- General exceptions are caught and logged, with a `500` status returned in the response.
- Inappropriate prompts are handled and return a `400` status with an error message.

## Usage Example
You can use tools like **Postman** or **cURL** to interact with the API.

Example `POST` request to generate an image:
```bash
curl -X POST http://localhost:5000/generate-image \
     -H "Content-Type: application/json" \
     -d '{"prompt": "Generate a futuristic football team logo"}'
```

The response will contain the filename to access the image:
```json
{
  "status": "success",
  "filename": "unique_image_id.png"
}
```

Example `GET` request to serve an image:
```bash
curl http://localhost:5000/images/unique_image_id.png
```

Example `GET` request for random prompts:
```bash
curl http://localhost:5000/generate-prompts
```

## To-Do (Future Enhancements)
- Add authentication for secure API access.
- Integrate Redis for caching frequently requested images.
- Implement additional image manipulation features (e.g., filters, color adjustments).
