import os
import sys
from os.path import join, dirname
from dotenv import load_dotenv
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

############################################################################
# API_KEYを設定
############################################################################
YOUR_CHANNEL_ACCESS_TOKEN = os.environ.get('YOUR_CHANNEL_ACCESS_TOKEN', None)
YOUR_CHANNEL_SECRET = os.environ.get('YOUR_CHANNEL_SECRET', None)
TALKAPI_KEY = os.environ.get('TALKAPI_KEY', None)
google_photo_client_id = os.environ.get('google_photo_client_id', None)
google_photo_client_secret = os.environ.get('google_photo_client_secret', None)
google_photo_album_id = os.environ.get('google_photo_album_id', None)
google_photo_refresh_token = os.environ.get('google_photo_refresh_token', None)
aws_s3_bucket = os.environ['AWS_BUCKET']

if YOUR_CHANNEL_ACCESS_TOKEN is None:
    print('Specify YOUR_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)
if YOUR_CHANNEL_SECRET is None:
    print('Specify YOUR_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if TALKAPI_KEY is None:
    print('Specify TALKAPI_KEY as environment variable.')
    sys.exit(1)
if google_photo_client_id is None:
    print('Specify GOOGLE_PHOTO_CLIENT_ID as environment variable.')
    sys.exit(1)
if google_photo_client_secret is None:
    print('Specify GOOGLE_PHOTO_CLIENT_SECRET as environment variable.')
    sys.exit(1)
if google_photo_album_id is None:
    print('Specify GOOGLE_PHOTO_ALBUM_ID as environment variable.')
    sys.exit(1)
if google_photo_refresh_token is None:
    print('Specify GOOGLE_PHOTO_REFRESH_TOKEN as environment variable.')
    sys.exit(1)
