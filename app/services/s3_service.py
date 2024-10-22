# -*- coding: utf-8 -*-
"""Service for uploading images to S3 bucket."""
import os
from io import BytesIO
import boto3

s3 = boto3.client('s3',
                  aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                  aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                  region_name=os.getenv('AWS_REGION'))

S3_BUCKET = os.getenv('S3_BUCKET_NAME')

def upload_image_to_s3(image_resized, unique_filename):
    """Upload image to S3 bucket."""
    # Save image to a BytesIO object to prepare for S3 upload
    image_byte_arr = BytesIO()
    image_resized.save(image_byte_arr, format="PNG")
    image_byte_arr.seek(0)

    # Upload image to S3
    s3.upload_fileobj(image_byte_arr, S3_BUCKET, unique_filename, ExtraArgs={"ContentType": "image/png"})
    
    s3_url = f"https://{S3_BUCKET}.s3.{os.getenv('AWS_REGION')}.amazonaws.com/{unique_filename}"
    return s3_url

def get_image_from_s3(filename):
    """Get image from S3 bucket."""
    s3_response = s3.get_object(Bucket=S3_BUCKET, Key=filename)
    image_data = s3_response['Body'].read()
    return image_data
