from flask import Flask, request, abort

import os

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,FollowEvent,
)

import openai   


app = Flask(__name__)

#need CHANNEL_ACCESS_TOKEN below
line_bot_api = LineBotApi('CHANNEL_ACCESS_TOKEN')
#need CHANNEL_SECRET bleow
handler = WebhookHandler('CHANNEL_SECRET')
#need OPEN-AI API KEY bleow
openai.api_key = "YOUR OPEN-AI API KEY"


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

@handler.add(FollowEvent)
def handle_follow(event):
    line_bot_api.reply_message(
    event.reply_token,
    TextSendMessage(text="Hello\n I'm your private ChatGPT."))
    
    
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text=event.message.text
    
    print('RUN')
    print(event.message)
    print(text)
    reply_text = chatgpt(text)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text))
    
    
def chatgpt(text):
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": text}
    ]
    )
    return completion.choices[0].message.content.strip()


if __name__ == "__main__":
    
    port = int(os.getenv("PORT", 4000))
    app.run(host="0.0.0.0", port=port)