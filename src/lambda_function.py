import pytesseract
import PIL.Image
import io
import os
from base64 import b64decode


LAMBDA_TASK_ROOT = os.environ.get('LAMBDA_TASK_ROOT', os.path.dirname(os.path.abspath(__file__)))
os.environ["PATH"] += os.pathsep + LAMBDA_TASK_ROOT


def lambda_handler(event, context):
  binary = b64decode(event['image64'])
  image = PIL.Image.open(io.BytesIO(binary))
  lang = event.get('lang', 'eng')
  text = pytesseract.image_to_string(image, lang=lang, config='--psm 6')
  return {'text' : text}
