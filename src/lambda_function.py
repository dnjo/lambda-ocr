import pytesseract
import os
import boto3
import logging
from PIL import Image

LAMBDA_TASK_ROOT = os.environ.get('LAMBDA_TASK_ROOT', os.path.dirname(os.path.abspath(__file__)))
os.environ["PATH"] += os.pathsep + LAMBDA_TASK_ROOT

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    s3_data = event['Records'][0]['s3']
    bucket_name = s3_data['bucket']['name']
    object_key = s3_data['object']['key']
    logger.info("Bucket = '%s', Key = '%s'", bucket_name, object_key)

    s3_client = boto3.client('s3')
    s3_response_object = s3_client.get_object(Bucket=bucket_name, Key=object_key)

    lang = s3_response_object['Metadata'].get('lang', 'eng')
    logger.info("Using language '%s'", lang)
    object_content = s3_response_object['Body']
    text = pytesseract.image_to_string(Image.open(object_content), lang=lang, config='--psm 6')

    logger.info("Image text: '%s'", text)
    return {'text': text}
