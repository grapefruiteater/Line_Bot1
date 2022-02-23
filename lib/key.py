import os
import sys

############################################################################
# API_KEYを設定
############################################################################
# get channel_secret and channel_access_token from your environment variable
channel_secret = os.environ.get('LINE_CHANNEL_SECRET', None)
channel_access_token = os.environ.get('LINE_CHANNEL_ACCESS_TOKEN', None)

if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)
if google_photo_client_id is None:
    print('Specify GOOGLE_PHOTO_CLIENT_ID as environment variable.')
    sys.exit(1)
