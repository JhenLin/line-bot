
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

line_bot_api = LineBotApi('gNtVJ95xJZMOzxpqGO1OhyVzrshRooI7XisCjktZDGDl9E/MKk/pGWECKB4DgYpUFB5fjP+lcuNv2jeB4y5fZlqzGr1hIdXVruC/tOvzFcOhwUtWCQe6gbMMGFhvQVwxC9RNrnt0MX6egJEnohTrFAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('583524f7788f8c0f4275c63cd71f3e07')


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
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()