from linebot import LineBotApi
from linebot.models import TextSendMessage    #テキストメッセージを送る時に使うモジュール
from linebot.exceptions import LineBotApiError

line_bot_api = LineBotApi('pxi09xpPSe/wloBZ0YHvjaJhHH+3t9QA1je/L0aqQfq0b0IE75cHhLUwaAhZKLnPjk0X/7rQqYUCHdcFX2m9kU/ZoqEyILX5mA3fOhMS5WcI/OyABSLREo1qVcGoKSbFopMEv1DQleRIbxpO7K99fQdB04t89/1O/w1cDnyilFU=')

try:
    # 該当botを友達追加している全員にメッセージを送る。
    line_bot_api.broadcast(TextSendMessage(text = "test message from python to all member"))

    # 特定の１ユーザーに送る時はこちら。その他にも、マルチキャスト、ナローキャストがある。
    # line_bot_api.push_message('<to>', TextSendMessage(text='test message from python to one user'))

except LineBotApiError as e:
    print(e)