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
    FlexSendMessage, TextSendMessage, QuickReply, QuickReplyButton, MessageAction, UnfollowEvent,
    CameraRollAction, CameraAction
)
from function import (
    func_registration_to_access, func_registration_data_collection_form
)
from database import (
    insert_db, update_db, get_value_db, remove_db
)
import requests, os, json
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

# Function to reply registration to access function call & initial follow event
def reply_greeting_message(event):
    line_bot_api.reply_message(
        event.reply_token,[
            TextSendMessage(text=f"👋🏻 สวัสดีครับคุณ {line_bot_api.get_profile(event.source.user_id).display_name} ✨ขอบคุณที่เป็นเพื่อนกับเราลงทะเบียนก่อนเข้าใช้งานในช่องแชทด้านล่างนี้ได้เลยครับ 💬"),
            FlexSendMessage(alt_text="Register to Access", contents=func_registration_to_access(), quick_reply=QuickReply(
                items=[
                    QuickReplyButton(action=MessageAction(label='🖊 ลงทะเบียนเข้าใช้งาน',text='ลงทะเบียนเข้าใช้งาน')),
                ]
            )),
        ]
    )

# Function to reply registration data collection form
def reply_registration_data_collection_form(event):
    line_bot_api.reply_message(
        event.reply_token,[
            FlexSendMessage(alt_text="คู่มือแบบฟอร์มการสมัครสมาชิก", contents=func_registration_data_collection_form())
        ]
    )

# Function to reply complete registration
def reply_registration_complete(event):
    line_bot_api.reply_message(
        event.reply_token,[
            TextSendMessage(text=f'💬 ลงทะเบียนเข้าใช้งานเสร็จสิ้น\n พิมพ์ `อัปโหลดรูปภาพ` หรือกดเมนูด้านล่างเพื่ออัปโหลดรูปภาพ', quick_reply=QuickReply(
                items=[
                    QuickReplyButton(action=MessageAction(label='✅ อัปโหลดรูปภาพ', text='อัปโหลดรูปภาพ')),
                ]
            ))
        ]
    )

# Function to reply error registration
def reply_registration_error(event):
    line_bot_api.reply_message(
        event.reply_token,[
            TextSendMessage(text='❌ ขออภัยระบบตรวจสอบการป้อนข้อมูลผิดพลาดกรุณาตรวจสอบข้อมูลและป้อนใหม่อีกครั้ง'),
        ]
    )

# Function to reply registration data collection form (isActive)
def reply_registration_data_collection_form_active(event, fullname, telephone, organization, farmer_code):
    line_bot_api.reply_message(
        event.reply_token,[
            FlexSendMessage(alt_text="Registration Data Form", contents=func_registration_data_collection_form(fullname, telephone, organization, farmer_code), quick_reply=QuickReply(
                items=[
                    QuickReplyButton(action=MessageAction(label='✅ ยืนยันการลงทะเบียน',text='ยืนยันการลงทะเบียน')),
                    QuickReplyButton(action=MessageAction(label='❌ ละทิ้งข้อมูลทั้งหมด',text='ละทิ้งข้อมูลทั้งหมด')),
                ]
            ))
        ]
    )

# Function validate data for commit registration 
def validate_commit_registration(text):
    return True

# Function record user in database 
def create_user_db(event):
    columns = "(user_id)"
    values = f"('{event.source.user_id}')"
    insert_db('users', columns, values)

# Function delete user in database 
def remove_user_db(event):
    columns = "(user_id)"
    values = f"'{event.source.user_id}'"
    remove_db('users', columns, values)

# Function to check registration status in database
def check_registration_status(event):
    table_name = "users"
    columns = "*"
    condition = f"user_id = '{event.source.user_id}'"

    for index in get_value_db(columns, table_name, condition):
        user_id = index[1]
        registration_status = index[3]
        fullname = index[4]
        telephone = index[5]
        organization = index[6]
        farmer_code = index[7]

    if(int(registration_status) == 1):
        return True
    else:
        if(event.message.type == "text"):
            # error
            if(event.message.text == "ลงทะเบียนเข้าใช้งาน"):
                reply_registration_data_collection_form(event)
                return False
            # error
            elif(event.message.text == "ยืนยันการลงทะเบียน"):
                update_db("users", "registration_status = 1", 'user_id', user_id)
                reply_registration_complete(event)
                return True
            # error
            elif(event.message.text == "ละทิ้งข้อมูลทั้งหมด"):
                update_db("users", f"fullname = NULL, telephone = NULL, organization = NULL, farmer_code = NULL", 'user_id', user_id)
                reply_registration_data_collection_form(event)
                return False
            else :
                if(validate_commit_registration(text=event.message.text)):
                    arr_text = event.message.text.split('\n')
                    # error -> list of out index here
                    fullname = arr_text[0]
                    telephone = arr_text[1]
                    organization = arr_text[2]
                    farmer_code = arr_text[3]
                    update_db("users", f"fullname = '{fullname}', telephone = '{telephone}', organization = '{organization}', farmer_code = '{farmer_code}'", 'user_id', user_id)
                    reply_registration_data_collection_form_active(event, fullname, telephone, organization, farmer_code)
                    return False
                else:
                    reply_registration_error(event)
                    return False

# Function to reply initial upload images
def reply_upload_images(event):
    line_bot_api.reply_message(
        event.reply_token,[
            TextSendMessage(text="💬 ท่านสามารถส่งภาพที่ต้องการโดยการอัปโหลดหรือถ่ายภาพผ่านช่องทางนี้ครับ", quick_reply=QuickReply(
                items=[
                    QuickReplyButton(action=CameraRollAction(label="เลือกภาพจากคลังรูปภาพ")),
                    QuickReplyButton(action=CameraAction(label="ถ่ายภาพ")),
                ]
            ))
        ]
    )

# Function to save images
def save_image(event):
    save_path = 'assets/images/'
    filename = f'{event.timestamp}.jpg'
    destination_path = os.path.join(save_path, filename)
    image_content = line_bot_api.get_message_content(event.message.id)
    with open(destination_path, 'wb') as fd:
        for chunk in image_content.iter_content():
            fd.write(chunk)

# Function to append json file
def append_data(event):
    json_path = 'image_files.json'
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            image_data = json.load(f)
    else:
        image_data = {}

    table_name = "users"
    columns = "*"
    condition = f"user_id = '{event.source.user_id}'"

    for index in get_value_db(columns, table_name, condition):
        farmer_code = index[7]
    

    if farmer_code in image_data:
        image_data[farmer_code].append({
            "image_path" : f"{event.timestamp}.jpg",
        })
    else:
        image_data[farmer_code] = [{
            "image_path" : f"{event.timestamp}.jpg",
        }]
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(image_data, f, ensure_ascii=False, indent=4)

# Function to update json file
def update_data(event):
    json_path = 'image_files.json'
    with open(json_path, 'r', encoding='utf-8') as f:
        image_data = json.load(f)

    table_name = "users"
    columns = "*"
    condition = f"user_id = '{event.source.user_id}'"
    for index in get_value_db(columns, table_name, condition):
        farmer_code = index[7]

    if farmer_code in image_data:
        for item in image_data[farmer_code]:
            if "latitude" not in item or item["latitude"] == "":
                item["latitude"] = event.message.latitude
            if "longitude" not in item or item["longitude"] == "":
                item["longitude"] = event.message.longitude
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(image_data, f, ensure_ascii=False, indent=4)
    return 

# Function to .post to web api
def post_information(event):
    json_path = 'image_files.json'
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            image_data = json.load(f)
    table_name = "users"
    columns = "*"
    condition = f"user_id = '{event.source.user_id}'"
    for index in get_value_db(columns, table_name, condition):
        farmer_code = index[7]
        for item in image_data[farmer_code]:
            print(farmer_code, item['image_path'])

@handler.add(FollowEvent)
def handle_follow_event(event):
    create_user_db(event)
    reply_greeting_message(event)
    return 200

@handler.add(UnfollowEvent)
def handle_unfollow_event(event):
    remove_user_db(event)
    return 200

@handler.add(MessageEvent,message=TextMessage)
def handle_text_event(event):
    if(check_registration_status(event)):
        user_message = event.message.text
        if(user_message == "อัปโหลดรูปภาพ"):
            reply_upload_images(event)

@handler.add(MessageEvent,message=LocationMessage)
def handle_location_event(event):
    if(check_registration_status(event)):
        update_data(event)
        post_information(event)
    return

@handler.add(MessageEvent,message=StickerMessage)
def handle_sticker_event(event):
    return

@handler.add(MessageEvent,message=ImageMessage)
def handle_image_event(event):
    if(check_registration_status(event)):
        save_image(event)
        append_data(event)
        
        return

if __name__ == '__main__':
    app.run(debug=True, port=8080)