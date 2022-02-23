import os
import sys
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(verbose=True, dotenv_path=dotenv_path)
############################################################################
# API_KEYを設定
############################################################################
YOUR_CHANNEL_ACCESS_TOKEN = os.environ.get('YOUR_CHANNEL_ACCESS_TOKEN', None)
YOUR_CHANNEL_SECRET = os.environ.get('YOUR_CHANNEL_SECRET', None)
TALKAPI_KEY = os.environ.get('TALKAPI_KEY', None)

if YOUR_CHANNEL_ACCESS_TOKEN is None:
    print('Specify YOUR_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)
if YOUR_CHANNEL_SECRET is None:
    print('Specify YOUR_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if TALKAPI_KEY is None:
    print('Specify TALKAPI_KEY as environment variable.')
    sys.exit(1)
