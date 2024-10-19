# Flask Image Generator API

This project provides a backend API built using **Flask** that integrates with **OpenAI's DALL-E** model to generate custom images based on user input. The API processes the generated image, makes the white background transparent, resizes it, and serves it through a unique URL. Additionally, Redis is used for caching, and MongoDB can be used for database storage.

## Features
- Generates images based on prompts using OpenAI's DALL-E API.
- Makes the background transparent and resizes images to 256x256 pixels.
- Saves images with unique filenames using UUIDs.
- Serves the generated images via a simple API endpoint.
- CORS enabled for cross-origin requests.

## Technologies
- **Flask**: Python web framework.
- **OpenAI API**: Used for generating images.
- **Pillow (PIL)**: Python Imaging Library for image manipulation.
- **UUID**: Ensures image filenames are unique.
- **Redis**: Caching system (optional integration).
- **MongoDB**: Optional database for storing image metadata (not yet used in this implementation).

## Endpoints

### `POST /generate-image`
Generates an image based on the provided prompt and returns a URL for accessing the generated image.

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
    "message": "Image generated and processed successfully.",
    "image_url": "http://localhost:5000/images/{uuid}.png"
  }
  ```

### `GET /images/<filename>`
Serves the image file stored on the server with the provided filename.

- **URL**: `http://localhost:5000/images/{uuid}.png`
- **Method**: GET
- **Response**: Returns the image file (PNG).

## Setup and Installation

### Prerequisites
- Python 3.x
- Flask
- Redis (optional)
- MongoDB (optional)

### Installation Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-repo/flask-image-generator.git
   cd flask-image-generator
   ```

2. **Create a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file in the root directory and add your OpenAI API key:
   ```bash
   OPENAI_API_KEY=your-openai-api-key
   ```

5. **Run the application**:
   ```bash
   flask run
   ```

6. The API should now be available at `http://localhost:5000`.

## Image Storage
Generated images are stored in the `images/` directory with filenames generated using UUID to ensure uniqueness.

## Usage Example
You can use tools like **Postman** or **cURL** to interact with the API.

Example `POST` request to generate an image:
```bash
curl -X POST http://localhost:5000/generate-image \
     -H "Content-Type: application/json" \
     -d '{"prompt": "Generate a futuristic football logo"}'
```

The response will contain the URL to access the image:
```json
{
  "status": "success",
  "message": "Image generated and processed successfully.",
  "image_url": "http://localhost:5000/images/unique_image_id.png"
}
```

## To-Do (Future Enhancements)
- Add authentication for secure API access.
- Store metadata (e.g., prompt, timestamp) in MongoDB.
- Implement image caching with Redis for faster retrieval.