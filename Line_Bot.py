
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import os
import requests

app = Flask(__name__)

#herokuの環境変数に設定された、LINE DevelopersのアクセストークンとChannelSecretを
#取得するコード
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]
line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

TALKAPI_KEY = 'DZZRwRUUUs8Xahfj1TQh9sqKgm2JUeHm'
def talkapi(text):
    url = 'https://api.a3rt.recruit.co.jp/talk/v1/smalltalk'
    req = requests.post(url, {'apikey':TALKAPI_KEY,'query':text}, timeout=5)
    data = req.json()
    if data['status'] != 0:
        return data['message']
    msg = data['results'][0]['reply']
    return msg

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
   push_text = event.message.text
   msg = talkapi(push_text)
   line_bot_api.reply_message(
       event.reply_token,
       TextSendMessage(text=msg))

def createRichmenu():
    result = False
    try:
        # define a new richmenu
        rich_menu_to_create = RichMenu(
            size = RichMenuSize(width=1200, height=405),
            selected = True,
            name = 'richmenu for randomchat',
            chat_bar_text = 'TAP HERE',
            areas=[
                RichMenuArea(
                    bounds=RichMenuBounds(x=0, y=0, width=480, height=405),
                    action=MessageAction(text=config.REMOVE)
                ),
                RichMenuArea(
                    bounds=RichMenuBounds(x=480, y=0, width=720, height=405),
                    action=MessageAction(text=config.NEXT)
                )
            ]
        )
        richMenuId = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_create)

        # upload an image for rich menu
        path = 'image path for richmenu'

        with open(path, 'rb') as f:
            line_bot_api.set_rich_menu_image(richMenuId, "image/jpeg", f)

        # set the default rich menu
        line_bot_api.set_default_rich_menu(richMenuId)

        result = True

    except Exception:
        result = False


    return result

# ポート番号の設定
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    
    # define a new richmenu
    rich_menu_to_create = RichMenu(
        size = RichMenuSize(width=1200, height=405),
        selected = True,
        name = 'richmenu for randomchat',
        chat_bar_text = 'TAP HERE',
        areas=[
            RichMenuArea(
                bounds=RichMenuBounds(x=0, y=0, width=480, height=405),
                action=MessageAction(text=config.REMOVE)
            ),
            RichMenuArea(
                bounds=RichMenuBounds(x=480, y=0, width=720, height=405),
                action=MessageAction(text=config.NEXT)
            )
        ]
    )
    richMenuId = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_create)
    
    path = 'https://github.com/grapefruiteater/Line_Bot1/blob/main/image/richmanu1.png'
    with open(path, 'rb') as f:
        line_bot_api.set_rich_menu_image(richMenuId, "image/png", f)
    line_bot_api.set_default_rich_menu(richMenuId)
