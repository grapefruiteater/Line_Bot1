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
    list_seki = {"seat":"1", "座席":"1", "席次":"1", "座席表":"1", "席次表":"1", "座席表を見せて":"1", "席次表を見せて":"1", "座席表をみせて":"1", "席次表をみせて":"1", "座席表みせて":"1", "席次表みせて":"1"}
    list_menu = {"menu":"1", "メニュー":"1", "メニュー表":"1", "メニューを見せて":"1", "メニュー表を見せて":"1", "メニュー表をみせて":"1", "メニューをみせて":"1", "メニューみせて":"1", "メニュー表みせて":"1"}
    if send_message in list_seki and isinstance(event.source, SourceUser):
        profile = line_bot_api.get_profile(event.source.user_id)
        tmpname = profile.display_name
        line_bot_api.reply_message(
            event.reply_token,
            ((TextSendMessage(text="%sさん! \n当日の席次表です。"%tmpname)),
                (ImageSendMessage(original_content_url="https://maindepository.s3.ap-northeast-1.amazonaws.com/table1.PNG",
                               preview_image_url="https://maindepository.s3.ap-northeast-1.amazonaws.com/table1.PNG"))))
    elif send_message in list_menu and isinstance(event.source, SourceUser):
        profile = line_bot_api.get_profile(event.source.user_id)
        tmpname = profile.display_name
        line_bot_api.reply_message(
            event.reply_token,
            ((TextSendMessage(text="%sさん! \n当日のメニュー表です。"%tmpname)),
                (ImageSendMessage(original_content_url="https://maindepository.s3.ap-northeast-1.amazonaws.com/%E7%B7%91+%E8%91%89%E3%81%AE%E3%83%9C%E3%83%BC%E3%83%80%E3%83%BC+%E7%B4%A0%E6%9C%B4%E3%81%AA%E8%8A%B1%E6%9F%84+%E7%B5%90%E5%A9%9A%E5%BC%8F%E5%B8%AD%E6%AC%A1%E8%A1%A8.png",
                               preview_image_url="https://maindepository.s3.ap-northeast-1.amazonaws.com/%E7%B7%91+%E8%91%89%E3%81%AE%E3%83%9C%E3%83%BC%E3%83%80%E3%83%BC+%E7%B4%A0%E6%9C%B4%E3%81%AA%E8%8A%B1%E6%9F%84+%E7%B5%90%E5%A9%9A%E5%BC%8F%E5%B8%AD%E6%AC%A1%E8%A1%A8.png"))))
    elif send_message == "Profile" and isinstance(event.source, SourceUser):
        profile = line_bot_api.get_profile(event.source.user_id)
        tmpname = profile.display_name
        line_bot_api.reply_message(
            event.reply_token,
            ((TextSendMessage(text="%sさん! \n敬太と希のプロフィールです。"%tmpname)),
                (ImageSendMessage(original_content_url="https://maindepository.s3.ap-northeast-1.amazonaws.com/table1.PNG",
                               preview_image_url="https://maindepository.s3.ap-northeast-1.amazonaws.com/table1.PNG"))))
    elif send_message == "招待状" and isinstance(event.source, SourceUser):
        profile = line_bot_api.get_profile(event.source.user_id)
        tmpname = profile.display_name
        line_bot_api.reply_message(
            event.reply_token,
            ((TextSendMessage(text="%sさん! \n招待状です。"%tmpname)),
                (ImageSendMessage(original_content_url="https://maindepository.s3.ap-northeast-1.amazonaws.com/table1.PNG",
                               preview_image_url="https://wedding-invi.jp/invitation/157639/0f92986ddf7"))))
    elif send_message == "写真・動画共有" and isinstance(event.source, SourceUser):
        line_bot_api.reply_message(
            event.reply_token,
            (TextSendMessage(text="写真・動画共有はここのチャットに送って頂ければ自動でレポジトリに追加されます。\n\nレポジトリは以下のURLから参照できます。\nhttps://bit.ly/3x1OWK4"))
            )
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
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='Correctly uploaded'))
    except: line_bot_api.reply_message(event.reply_token,TextSendMessage(text='Failure uploaded'))

@handler.add(MessageEvent, message=VideoMessage)
def handle_image_message(event):
    display_name = 'None'
    if isinstance(event.source, SourceUser):
        profile = line_bot_api.get_profile(event.source.user_id)
        user_id = event.source.user_id
        display_name = profile.display_name
    else: print("user profile can't not use")
    message_content = line_bot_api.get_message_content(event.message.id)
    Video_data = line_bot_api.get_message_content(event.message.id).iter_content()
    src_img_path = "./image/sample.mp4"
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
    Key = '%s_%s.mp4'%(display_name,event.message.id)
    try:
        client.upload_file(src_img_path, Bucket, Key)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='Correctly uploaded'))
    except: line_bot_api.reply_message(event.reply_token,TextSendMessage(text='Failure uploaded'))        

@handler.add(FollowEvent)
def handle_follow(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='登録して頂きありがとうございます！\nこれは敬太と希の結婚式のLINE公式アカウントです。\n下記のメニューから会場場所や座席表、お写真や動画の共有ができます。\nぜひご活用頂ければと思います。'))

   
# ポート番号の設定
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
