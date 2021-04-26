from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import mongodb
import re
from gevent import pywsgi

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('LINE_CHANNEL_ACCESS_TOKEN')
# Channel Secret
handler = WebhookHandler('LINE_CHANNEL_SECRET')
yourid='你的User ID'
line_bot_api.push_message(yourid, TextSendMessage(text='你可以開始了'))

# 監聽所有來自 /callback 的 Post Request
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

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)

def handle_message(event):
    profile = line_bot_api.get_profile(event.source.user_id)
    #message = TextSendMessage(text=event.message.text)
    #uid = 'Uebfe00aa315160471e0981c1c28e3084'
    uid = profile.user_id
    usespeak=str(event.message.text)
    if re.match('[0-9]{4}[<>][0-9]',usespeak):
        mongodb.write_user_stock_function(stock=usespeak[0:4], bs=usespeak[4:5],price=usespeak[5:])
        line_bot_api.push_message(uid, TextSendMessage(usespeak[0:4]+'已經儲存成功'))
        return 0
    elif re.match('刪除[0-9]{4}',usespeak):
        mongodb.delete_user_stock_function(stock=usespeak[2:])
        line_bot_api.push_message(uid, TextSendMessage(usespeak+'已經刪除成功'))
        return 0
    

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='127.0.0.1', port=port)    
