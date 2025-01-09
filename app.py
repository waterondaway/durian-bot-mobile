from flask import (
    Flask, abort, request
)
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError, LineBotApiError
)
from linebot.models import (
    MessageEvent, FollowEvent, TextMessage, ImageMessage, LocationMessage, StickerMessage,
    FlexSendMessage, TextSendMessage, QuickReply, QuickReplyButton, MessageAction
)
from function import (
    func_registration_to_access
)
import requests, os
# Load environment from .env file ------
from dotenv import load_dotenv
load_dotenv()

# Turn OFF Warning ---------------------
import warnings
warnings.filterwarnings('ignore')

# Main Execution -----------------------
app = Flask(__name__)

# API Key Configuration --------------------
line_bot_api = LineBotApi(os.getenv('channel_access_token'))
handler = WebhookHandler(os.getenv('channel_secret'))

# Function to reply registration to access function call & initial follow event
def reply_registration_to_access(event):
    line_bot_api.reply_message(
        event.reply_token,[
            FlexSendMessage(alt_text="hello", contents=func_registration_to_access(), quick_reply=QuickReply(
                items=[
                    QuickReplyButton(action=MessageAction(label='🖊 ลงทะเบียนเข้าใช้งาน',text='ลงทะเบียนเข้าใช้งาน')),
                    QuickReplyButton(action=MessageAction(label='❌ ละทิ้งข้อมูลทั้งหมด',text='ละทิ้งข้อมูลทั้งหมด')),
                ]
            )),
        ]
    )
    return

# Function to reply registration data collection form
def reply_registration_data_collection_form(event):
    return
@app.route('/',methods=['GET'])
def default():
    return 'Hello World!'

@app.route("/callback",methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except LineBotApiError as e:
        print("Got exception from LINE Messaging API: %s\n" % e.message)
        for m in e.error.details:
            print("  %s: %s" % (m.property, m.message))
        print("\n")
    except Exception as error:
        print(error)
        abort(400)
    return 'OK', 200

@handler.add(FollowEvent)
def handle_follow_event(event):
    reply_registration_to_access(event)
    return

@handler.add(MessageEvent,message=TextMessage)
def handle_text_event(event):
    reply_registration_to_access(event)
    return


@handler.add(MessageEvent,message=LocationMessage)
def handle_location_event(event):
    return

@handler.add(MessageEvent,message=StickerMessage)
def handle_sticker_event(event):
    return

if __name__ == '__main__':
    app.run(debug=True, port=8080)