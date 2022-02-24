from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageTemplateAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URITemplateAction,
    PostbackTemplateAction, DatetimePickerTemplateAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage, ImageSendMessage, VideoSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent
)

from linebot.models import RichMenu, RichMenuArea, RichMenuBounds, RichMenuSize,URIAction
from linebot.models import CameraAction, CameraRollAction
from linebot.models.actions import PostbackAction

import os
import requests
import urllib
import urllib.request
from lib import photo
import boto3

app = Flask(__name__)

#herokuに設定された環境変数を呼び出す
from lib.key import (
    YOUR_CHANNEL_ACCESS_TOKEN, YOUR_CHANNEL_SECRET, TALKAPI_KEY, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION
)

#YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
#YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]
line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

#TALKAPI_KEY = os.environ["TALKAPI_KEY"]
def talkapi(text):
    url = 'https://api.a3rt.recruit.co.jp/talk/v1/smalltalk'
    req = requests.post(url, {'apikey':TALKAPI_KEY,'query':text}, timeout=5)
    data = req.json()
    if data['status'] != 0:
        return data['message']
    rep = data['results'][0]['reply']
    return rep

#herokuへのデプロイが成功したかどうかを確認するためのコード
@app.route("/")
def hello_world():
    return "hello world!"


#LINE DevelopersのWebhookにURLを指定してWebhookからURLにイベントが送られるようにする
@app.route("/callback", methods=['POST'])
def callback():
    # リクエストヘッダーから署名検証のための値を取得
    signature = request.headers['X-Line-Signature']

    # リクエストボディを取得
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # 署名を検証し、問題なければhandleに定義されている関数を呼ぶ
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


#以下でWebhookから送られてきたイベントをどのように処理するかを記述する
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    send_message = event.message.text
    rep = talkapi(send_message)
    display_name = 'None'
    if isinstance(event.source, SourceUser):
        profile = line_bot_api.get_profile(event.source.user_id)
        user_id = event.source.user_id
        display_name = profile.display_name
    else: print("user profile can't not use")
    if send_message == "座席表" and isinstance(event.source, SourceUser):
        profile = line_bot_api.get_profile(event.source.user_id)
        tmpname = profile.display_name
        line_bot_api.reply_message(
            event.reply_token,
            ((TextSendMessage(text="Thank you %s!. Here is seat plan on reception."%tmpname)),
                (ImageSendMessage(original_content_url="https://maindepository.s3.ap-northeast-1.amazonaws.com/table1.PNG",
                               preview_image_url="https://maindepository.s3.ap-northeast-1.amazonaws.com/table1.PNG"))))
    elif send_message == "メニュー表" and isinstance(event.source, SourceUser):
        profile = line_bot_api.get_profile(event.source.user_id)
        tmpname = profile.display_name
        line_bot_api.reply_message(
            event.reply_token,
            ((TextSendMessage(text="Thank you %s!. Here is seat plan on reception."%tmpname)),
                (ImageSendMessage(original_content_url="https://maindepository.s3.ap-northeast-1.amazonaws.com/table1.PNG",
                               preview_image_url="https://maindepository.s3.ap-northeast-1.amazonaws.com/table1.PNG"))))
    elif send_message == "Profile" and isinstance(event.source, SourceUser):
        profile = line_bot_api.get_profile(event.source.user_id)
        tmpname = profile.display_name
        line_bot_api.reply_message(
            event.reply_token,
            ((TextSendMessage(text="Thank you %s!. Here is seat plan on reception."%tmpname)),
                (ImageSendMessage(original_content_url="https://maindepository.s3.ap-northeast-1.amazonaws.com/table1.PNG",
                               preview_image_url="https://maindepository.s3.ap-northeast-1.amazonaws.com/table1.PNG"))))
    elif send_message == "Time Table" and isinstance(event.source, SourceUser):
        profile = line_bot_api.get_profile(event.source.user_id)
        tmpname = profile.display_name
        line_bot_api.reply_message(
            event.reply_token,
            ((TextSendMessage(text="Thank you %s!. Here is seat plan on reception."%tmpname)),
                (ImageSendMessage(original_content_url="https://maindepository.s3.ap-northeast-1.amazonaws.com/table1.PNG",
                               preview_image_url="https://maindepository.s3.ap-northeast-1.amazonaws.com/table1.PNG"))))
    else:
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=rep))

@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    display_name = 'None'
    if isinstance(event.source, SourceUser):
        profile = line_bot_api.get_profile(event.source.user_id)
        user_id = event.source.user_id
        display_name = profile.display_name
    else: print("user profile can't not use")
    message_content = line_bot_api.get_message_content(event.message.id)
    img_data = line_bot_api.get_message_content(event.message.id).iter_content()
    src_img_path = "./image/sample.png"
    with open(src_img_path, "wb") as f:
        for chunk in message_content.iter_content():
            f.write(chunk)
    client = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_DEFAULT_REGION
    )
    Bucket = 'linebotphoto'
    Key = '%s_%s.png'%(display_name,event.message.id)
    try:
        client.upload_file(src_img_path, Bucket, Key)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='Correctly uploaded!!!'))
    except: line_bot_api.reply_message(event.reply_token,TextSendMessage(text='Failure uploaded!!!'))
            
@handler.add(FollowEvent)
def handle_follow(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='Hello'))

   
# ポート番号の設定
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
