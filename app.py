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

line_bot_api = LineBotApi('ZPCO/uhOXnZ4c7N8+xrzC8Ij8SQ83awTx4egglS22qaTQEFnHAUqrsH+7/bxSSUJFprCKC+cCBIQOegMu24ceO2dfqZ+OeMZSGtqV4GBgNSyR6JKb0uOS/6g8uKcvIYaPsvdHDl536gDz8s53pBqfgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('c559137451dc240917c11f83ac121a92')


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
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()