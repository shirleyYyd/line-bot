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

app = Flask(__name__)
#token 權杖
#secret 存取秘密
line_bot_api = LineBotApi('ktwIGGqsjMlhY866x02hzkBQUOAOfqrw9QO+pla/PM8/Kw+UBs2f6OeCW8/5J1HLzr1mpB2YpiI6j1ZVSFr015QkqbTQTEKUuI7qz6Qq8CubyC4ZpBPjSwq7LpjOkat7MYwvFu++eZjkhuAECsByHAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('f2e0aed11a828a0d50951b70f41c14d7')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    r = '很抱歉，我不太懂您的意思'#預設回傳訊息
    if '給我貼圖' in msg:
        sticker_message = StickerSendMessage(
            package_id='1',
            sticker_id='1'
        )

        line_bot_api.reply_message(
        event.reply_token,
        sticker_message)

        return

    if msg in ['hi', 'Hi']:
        r = '嗨~'
    elif msg in ['你吃飯了嗎', '你睡了嗎', '你上班了嗎', '你下班了嗎', '你吃了嗎']:
        r = '還沒'
    elif msg in ['你是誰', 'who are you', 'Who are you', '你誰', '你是']:
        r = '我是機器人'
    elif '訂位' in msg:
        r = '您想要訂位嗎？' 

    elif '漂亮' in msg:
        r = '謝謝'

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text = r))


if __name__ == "__main__":
    app.run()

