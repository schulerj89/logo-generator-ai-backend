"""Flask configuration variables."""
import os

# pylint: disable=too-few-public-methods
class Config:
    """Set Flask configuration vars from .env file."""
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_REGION = os.getenv('AWS_REGION')
    S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')
