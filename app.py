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
    func_registration_to_access, func_registration_data_collection_form
)
from database import (
    insert_db, update_db, get_value_db
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
            TextSendMessage(text=f"👋🏻 สวัสดีครับคุณ {line_bot_api.get_profile(event.source.user_id).display_name} ✨ขอบคุณที่เป็นเพื่อนกับเราลงทะเบียนก่อนเข้าใช้งานในช่องแชทด้านล่างนี้ได้เลยครับ 💬"),
            FlexSendMessage(alt_text="Register to Access", contents=func_registration_to_access(), quick_reply=QuickReply(
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
    line_bot_api.reply_message(
        event.reply_token,[
            FlexSendMessage(alt_text="Registration Data Form", contents=func_registration_data_collection_form(), quick_reply=QuickReply(
                items=[
                    QuickReplyButton(action=MessageAction(label='✅ ยืนยันการลงทะเบียน',text='ยืนยันการลงทะเบียน')),
                    QuickReplyButton(action=MessageAction(label='❌ ละทิ้งข้อมูลทั้งหมด',text='ละทิ้งข้อมูลทั้งหมด')),
                ]
            ))
        ]
    )
    return

# Function to reply complete registration
def reply_registration_complete(event):
    line_bot_api.reply_message(
        event.reply_token,[
            TextSendMessage(text=f'💬 ลงทะเบียนเข้าใช้งานเสร็จสิ้น\n พิมพ์ `เริ่มต้นใช้งาน` หรือกดเมนูด้านล่างเพื่อเริ่มต้นการใช้งาน', quick_reply=QuickReply(
                items=[
                    QuickReplyButton(action=MessageAction(label='✅ เริ่มต้นใช้งาน', text='เริ่มต้นใช้งาน')),
                    QuickReplyButton(action=MessageAction(label='⚙️ คู่มือการใช้งาน', text='คู่มือการใช้งาน'))
                ]
            ))
        ]
    )
    return

# Function to reply error registration
def reply_registration_error(event):
    line_bot_api.reply_message(
        event.reply_token,[
            TextSendMessage(text='❌ ขออภัยระบบตรวจสอบการป้อนข้อมูลผิดพลาดกรุณาตรวจสอบข้อมูลและป้อนใหม่อีกครั้ง'),
            FlexSendMessage(alt_text="Registration Data Form", contents=func_registration_data_collection_form(), quick_reply=QuickReply(
                items=[
                    QuickReplyButton(action=MessageAction(label='✅ ยืนยันการลงทะเบียน',text='ยืนยันการลงทะเบียน')),
                    QuickReplyButton(action=MessageAction(label='❌ ละทิ้งข้อมูลทั้งหมด',text='ละทิ้งข้อมูลทั้งหมด')),
                ]
            ))
            
        ]
    )
    return

# Function to reply registration data collection form (isActive)
def reply_registration_data_collection_form_active(event):
    arr_text = event.message.text.split('\n')
    fullname = arr_text[0]
    telephone = arr_text[1]
    organization = arr_text[2]
    line_bot_api.reply_message(
        event.reply_token,[
            FlexSendMessage(alt_text="Registration Data Form", contents=func_registration_data_collection_form(fullname, telephone, organization), quick_reply=QuickReply(
                items=[
                    QuickReplyButton(action=MessageAction(label='✅ ยืนยันการลงทะเบียน',text='ยืนยันการลงทะเบียน')),
                    QuickReplyButton(action=MessageAction(label='❌ ละทิ้งข้อมูลทั้งหมด',text='ละทิ้งข้อมูลทั้งหมด')),
                ]
            ))
        ]
    )
    return

# Function validate data for commit registration 
def validate_commit_registration(event):
    return True

# Function record user in database 
def create_user_db(event):
    columns = "(user_id)"
    values = f"('{event.source.user_id}')"
    insert_db('users', columns, values)
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
    create_user_db(event)
    reply_registration_to_access(event)
    return

@handler.add(MessageEvent,message=TextMessage)
def handle_text_event(event):
    # reply_registration_to_access(event)
    if(event.message.text == 'ลงทะเบียนเข้าใช้งาน'):
        reply_registration_data_collection_form(event)
    elif(event.message.text == 'ละทิ้งข้อมูลทั้งหมด'):
        reply_registration_data_collection_form(event)
    elif(event.message.text == 'ยืนยันการลงทะเบียน'):
        if validate_commit_registration(event): 
            reply_registration_complete(event)
        else: 
            reply_registration_error(event)
    else:
        reply_registration_data_collection_form_active(event)
    return

@handler.add(MessageEvent,message=LocationMessage)
def handle_location_event(event):
    return

@handler.add(MessageEvent,message=StickerMessage)
def handle_sticker_event(event):
    return

if __name__ == '__main__':
    app.run(debug=True, port=8080)