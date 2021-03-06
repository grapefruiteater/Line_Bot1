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
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent, FlexSendMessage
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
import json

#from fastapi import FastAPI, Request, BackgroundTasks
#from aiolinebot import AioLineBotApi
#app = FastAPI()
app = Flask(__name__)

#herokuに設定された環境変数を呼び出す
from lib.key import (
    YOUR_CHANNEL_ACCESS_TOKEN, YOUR_CHANNEL_SECRET, TALKAPI_KEY, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION
)

#YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
#YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]
line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

#line_bot_api = AioLineBotApi(channel_access_token=os.environ.get("YOUR_CHANNEL_ACCESS_TOKEN"))
#parser = WebhookParser(channel_secret=os.environ.get("YOUR_CHANNEL_SECRET"))

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
                (ImageSendMessage(original_content_url="https://maindepository.s3.ap-northeast-1.amazonaws.com/seat_plan.jpg",
                               preview_image_url="https://maindepository.s3.ap-northeast-1.amazonaws.com/seat_plan.jpg"))))
    elif send_message in list_menu and isinstance(event.source, SourceUser):
        profile = line_bot_api.get_profile(event.source.user_id)
        tmpname = profile.display_name
        line_bot_api.reply_message(
            event.reply_token,
            ((TextSendMessage(text="%sさん! \n当日のメニュー表です。"%tmpname)),
                (ImageSendMessage(original_content_url="https://maindepository.s3.ap-northeast-1.amazonaws.com/Wedding+Menu.jpg",
                               preview_image_url="https://maindepository.s3.ap-northeast-1.amazonaws.com/Wedding+Menu.jpg"))))
    elif send_message == "Profile" and isinstance(event.source, SourceUser):
        profile = line_bot_api.get_profile(event.source.user_id)
        tmpname = profile.display_name
        line_bot_api.reply_message(
            event.reply_token,
            ((TextSendMessage(text="%sさん! \n敬太と希のプロフィールです。"%tmpname)),
                (ImageSendMessage(original_content_url="https://maindepository.s3.ap-northeast-1.amazonaws.com/Profile.jpg",
                               preview_image_url="https://maindepository.s3.ap-northeast-1.amazonaws.com/Profile.jpg"))))
    elif send_message == "招待状" and isinstance(event.source, SourceUser):
        profile = line_bot_api.get_profile(event.source.user_id)
        tmpname = profile.display_name
        line_bot_api.reply_message(
            event.reply_token,
            ((TextSendMessage(text="%sさん! \n招待状です。"%tmpname)),
                (ImageSendMessage(original_content_url="https://wedding-invi.jp/invitation/157639/0f92986ddf7",
                               preview_image_url="https://wedding-invi.jp/invitation/157639/0f92986ddf7"))))
    elif send_message == "写真・動画共有" and isinstance(event.source, SourceUser):
        line_bot_api.reply_message(
            event.reply_token,
            (TextSendMessage(text="写真・動画共有はここのチャットに送って頂ければ自動でレポジトリに追加されます。")) 
            )
    elif send_message == "何時に行けばいいですか？":
        line_bot_api.reply_message(
            event.reply_token,
            (TextSendMessage(text='9:30~10:30の間にラグナヴェール広島へお越しください。会場へのアクセスは結婚式公式アカウントのメニュー右下の"会場場所・アクセス"からGoogle Mapが確認できます。'))
            )
    elif send_message == "服装はどうしたらいいですか？":
        line_bot_api.reply_message(
            event.reply_token,
            (TextSendMessage(text='基本的には自由です。男性はスーツ、女性はドレスを召してお越し頂けると幸いです。'))
            )
    elif send_message == "ご祝儀はどうしたらいいですか？":
        line_bot_api.reply_message(
            event.reply_token,
            (TextSendMessage(text='当日、受付にてお渡し頂ければ幸いです。'))
            )
    elif send_message == "よくある質問" and isinstance(event.source, SourceUser):
        bubble_string = """
            {
              "type": "bubble",
              "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": "よくある質問",
                    "weight": "bold",
                    "align": "center",
                    "color": "#ffffff"
                  },
                  {
                    "type": "text",
                    "text": "お困りの状況に該当するものをお選びください。",
                    "wrap": true,
                    "color": "#ffffff"
                  }
                ],
                "backgroundColor": "#00CC62"
              },
              "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                      {
                        "type": "text",
                        "text": "何時に行けばいいですか？",
                        "align": "center",
                        "color": "#42659a"
                      }
                    ],
                    "action": {
                      "type": "postback",
                      "label": "question",
                      "data": "action=question&id=1",
                      "displayText": "何時に行けばいいですか？"
                    }
                  },
                  {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                      {
                        "type": "text",
                        "text": "駐車場はありますか？",
                        "color": "#42659a",
                        "align": "center"
                      }
                    ],
                    "margin": "12px",
                    "action": {
                      "type": "postback",
                      "label": "question",
                      "data": "action=question&id=2",
                      "displayText": "駐車場はありますか？"
                    }
                  },
                  {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                      {
                        "type": "text",
                        "text": "服装はどうしたらいいですか？",
                        "color": "#42659a",
                        "align": "center"
                      }
                    ],
                    "margin": "12px",
                    "action": {
                      "type": "postback",
                      "label": "question",
                      "data": "action=question&id=3",
                      "displayText": "服装はどうしたらいいですか？"
                    }
                  },
                  {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                      {
                        "type": "text",
                        "text": "ご祝儀はどうしたらいいですか？",
                        "align": "center",
                        "color": "#42659a"
                      }
                    ],
                    "margin": "12px",
                    "action": {
                      "type": "postback",
                      "label": "question",
                      "data": "action=question&id=4",
                      "displayText": "ご祝儀はどうしたらいいですか？"
                    }
                  }
                ]
              }
            }
        """
        message = FlexSendMessage(alt_text="よくある質問", contents=json.loads(bubble_string))
        line_bot_api.reply_message(
            event.reply_token,
            message
        )
    else:
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=rep))

@handler.add(PostbackEvent)
def handle_postback(event):
    if event.postback.data == 'action=question&id=1':
        line_bot_api.reply_message(
            event.reply_token,
            (TextSendMessage(text='9:30~10:30の間にラグナヴェール広島へお越しください。会場へのアクセスは結婚式公式アカウントのメニュー右下の"会場場所・アクセス"からGoogle Mapが確認できます。'))
        )
    elif event.postback.data == 'action=question&id=2':
        line_bot_api.reply_message(
            event.reply_token,
            (TextSendMessage(text='会場には無料駐車場はございません。会場の左隣に有料の立体駐車場があります。その他でも、お近くの有料駐車場にお停めいただければ大丈夫です。'))
        )
    elif event.postback.data == 'action=question&id=3':
        line_bot_api.reply_message(
            event.reply_token,
            (TextSendMessage(text='基本的には自由です。男性はスーツ、女性はドレスを召してお越し頂けると幸いです。'))
        )
    elif event.postback.data == 'action=question&id=4':
        line_bot_api.reply_message(
            event.reply_token,
            (TextSendMessage(text='大変お手数ですがご祝儀袋をご用意頂き、当日会場の受付にて担当者にお渡しください。以下に参考としてご祝儀袋のリンクを張っておりますので、良ければご利用ください。\nhttps://amzn.to/36rzbBh'))
        )        
        
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
        TextSendMessage(text='登録して頂きありがとうございます！これは敬太と希の結婚式のLINE公式アカウントです。\n\n下記Menuから会場場所や席次表、料理メニューのご確認、お写真・動画のご共有ができます。お困りの際は"よくある質問"と話しかけていただければ幸いです。\n\n自動会話AIと連携しているので、暇なときにチャットで話しかけてみてください。\n\nぜひご活用頂ければ幸いです。'))

   
# ポート番号の設定
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
