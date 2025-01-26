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
    CameraRollAction, CameraAction, TemplateSendMessage, ButtonsTemplate, URIAction, LocationAction
)

import os, json
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

@app.route("/callback",methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    #app.logger.info("Request body: " + body)
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
            # TextSendMessage(text=f"👋🏻 สวัสดีครับคุณ {line_bot_api.get_profile(event.source.user_id).display_name} ✨ ขอบคุณที่เป็นเพื่อนกับเราลงทะเบียนก่อนเข้าใช้งานในช่องแชทด้านล่างนี้ได้เลยครับ"),
            TextSendMessage(text=f"👋🏻 สวัสดีครับคุณ {line_bot_api.get_profile(event.source.user_id).display_name} ✨ ขอบคุณที่เป็นเพื่อนกับเราลงทะเบียนก่อนเข้าใช้งานในช่องแชทด้านล่างนี้ได้เลยครับ",quick_reply=QuickReply(
                items=[
                    QuickReplyButton(action=MessageAction(label="อัปโหลดข้อมูล",text="upload"))
                ]
            )),
            # FlexSendMessage(alt_text="แบบฟอร์มลงทะเบียนเข้าใช้งาน", contents=func_registration_to_access(), quick_reply=QuickReply(
            #     items=[
            #         QuickReplyButton(action=MessageAction(label='🖊 ลงทะเบียนเข้าใช้งาน',text='ลงทะเบียนเข้าใช้งาน')),
            #     ]
            # )),
        ]
    )

# Function to check registration status
def function_validate_registration_status(event):
    return True

# Function to reply unregistration
def reply_unregistration(event):
    line_bot_api.reply_message(
        event.reply_token,[
            TextSendMessage(text="💬 ระบบร้องขอให้ผู้ใช้งานลงทะเบียนเข้าใช้ ก่อนเริ่มทำการใช้งานครับ")
        ]
    )

# Function to save images
def function_save_image(event):
    save_path = 'assets/image/'
    filename = f'{event.timestamp}.jpg'
    destination_path = os.path.join(save_path, filename)
    image_content = line_bot_api.get_message_content(event.message.id)
    with open(destination_path, 'wb') as fd:
        for chunk in image_content.iter_content():
            fd.write(chunk)
# Function to append data (image) to json file
def function_append_image_json(event):
    json_path = 'image.json'

    with open(json_path, 'r', encoding='utf-8') as f:
        image_json = json.load(f)
 
    if "images" in image_json[event.source.user_id]:
        image_json[event.source.user_id]["images"].append(f"{event.timestamp}.jpg")
    else:
        image_json[event.source.user_id]["images"] = [f"{event.timestamp}.jpg"]
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(image_json, f, ensure_ascii=False, indent=4)

# Function to check valid/invalid append or update to json file
def function_validate_key_json(event):
    json_path = 'image.json'
    with open(json_path, 'r', encoding='utf-8') as f:
            image_json = json.load(f)
    if event.source.user_id in image_json:
        return True
    else:
        return False
    
# Function to append data (location) to json file 
def function_append_location_json(event):
    json_path = 'image.json'
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            image_json = json.load(f)
    
    image_json[event.source.user_id]["location"] = {
        "latitude" : event.message.latitude,
        "longitude" : event.message.longitude
    }

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(image_json, f, ensure_ascii=False, indent=4)

# Function to create key to json file
def function_create_key_json(event):
    json_path = 'image.json'
    with open(json_path, 'r', encoding='utf-8') as f:
        image_json = json.load(f)
    image_json[event.source.user_id] = {}

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(image_json, f, ensure_ascii=False, indent=4)
    return True

# Function to reply already have key in json file
def reply_already_key_json(event):
    line_bot_api.reply_message(
        event.reply_token,[
            TextSendMessage(text="💬 ระบบตรวจพบการร้องขอไว้ก่อนหน้าแล้ว ท่านสามารถอัปโหลดรูปภาพที่ต้องการและตำแหน่งที่ตั้งของท่านได้เลยครับ",quick_reply=QuickReply(
                items=[
                    QuickReplyButton(action=CameraAction(label="Camera")),
                    QuickReplyButton(action=CameraRollAction(label="Camera Roll")),
                    QuickReplyButton(action=LocationAction(label="Location"))
                ]
            ))
        ]
    )

# Function to reply ready for upload
def reply_ready_upload(event):
    line_bot_api.reply_message(
        event.reply_token,[
            TextSendMessage(text="💬 ระบบพร้อมอัปโหลดรูปภาพและตำแหน่งที่ตั้งของท่านแล้วครับ",quick_reply=QuickReply(
                items=[
                    QuickReplyButton(action=CameraAction(label="Camera")),
                    QuickReplyButton(action=CameraRollAction(label="Camera Roll")),
                    QuickReplyButton(action=LocationAction(label="Location"))
                ]
            ))
        ]
    )

def reply_upload_images(event):
    line_bot_api.reply_message(
        event.reply_token,[
            TextSendMessage(text="💬 อัปโหลดรูปภาพดังกล่าวแล้ว",quick_reply=QuickReply(
                items=[
                    QuickReplyButton(action=CameraAction(label="Camera")),
                    QuickReplyButton(action=CameraRollAction(label="Camera Roll")),
                    QuickReplyButton(action=LocationAction(label="Location")),
                    QuickReplyButton(action=MessageAction(label="Submit",text="submit")),
                ]
            ))
        ]
    )
# Function to reply unalready have key in json file
def reply_unalready_key_json(event):
    line_bot_api.reply_message(
        event.reply_token,[
            TextSendMessage(text="💬 ระบบไม่พบการร้องขออัปโหลดรูปภาพ กรุณาพิมพ์ 'upload' ก่อนครับ",quick_reply=QuickReply(
                items=[
                    QuickReplyButton(action=MessageAction(label="อัปโหลดข้อมูล",text="upload"))
                ]
            ))
        ]
    )

# Function to reply upload data complete
def reply_upload_complete(event):
    line_bot_api.reply_message(
        event.reply_token,[
            TextSendMessage(text="💬 ระบบอัปโหลดรูปภาพของท่านแล้วครับ")
        ]
    )

# Function to check all data have value in json file
def function_validate_complete_json(event):
    json_path = 'image.json'
    with open(json_path, 'r', encoding='utf-8') as f:
        image_json = json.load(f)
    if "images" in image_json[event.source.user_id] and "location" in image_json[event.source.user_id]:
        return True
    else:
        return False


# Function to reply upload data failed
def reply_upload_failed(event):
    line_bot_api.reply_message(
        event.reply_token,[
            TextSendMessage(text="💬 ระบบตรวจพบข้อมูลยังไม่ครบกรุณากรอกข้อมูลให้ครบถ้วนก่อนครับ",quick_reply=QuickReply(
                items=[
                    QuickReplyButton(action=CameraAction(label="Camera")),
                    QuickReplyButton(action=CameraRollAction(label="Camera Roll")),
                    QuickReplyButton(action=LocationAction(label="Location")),
                ]
            ))
        ]
    )

# Function to remove key in json file
def function_remove_key_json(event):
    json_path = 'image.json'
    with open(json_path, 'r', encoding='utf-8') as f:
        image_json = json.load(f)

    del image_json[event.source.user_id]

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(image_json, f, ensure_ascii=False, indent=4)

# Function to post image to server
def function_post_image(event):
    return 

@handler.add(FollowEvent)
def handle_follow_event(event):
    reply_greeting_message(event)
    return 200

@handler.add(UnfollowEvent)
def handle_unfollow_event(event):
    function_remove_key_json(event)
    return 200

@handler.add(MessageEvent, message=TextMessage)
def handle_text_event(event):
    if(function_validate_registration_status(event)):
        print(f"\nTextMessage from {event.source.user_id} | Message : {event.message.text}")

        if(event.message.text == "upload"):
            if(function_validate_key_json(event) == False):
                function_create_key_json(event)
                reply_ready_upload(event)
            else:
                reply_already_key_json(event)
        elif(event.message.text == "submit"):
            if(function_validate_key_json(event)):
                if(function_validate_complete_json(event)):
                    function_post_image(event)
                    reply_upload_complete(event)
                    function_remove_key_json(event)
                else:
                    reply_upload_failed(event)
            else:
                reply_unalready_key_json(event)
    else:
        print(f"\nUnregistration User | TextMessage from {event.source.user_id} | Message : {event.message.text}")
        reply_unregistration(event)

    return 200

@handler.add(MessageEvent, message=LocationMessage)
def handle_location_event(event):
    if(function_validate_registration_status(event)):
        print(f"\nLocationMessage from {event.source.user_id} | Location : {event.message.latitude} {event.message.longitude}")
        if function_validate_key_json(event):
            function_append_location_json(event)
            reply_upload_images(event)
        else:
            reply_unalready_key_json(event)
    else:
        print(f"\nUnregistration User | LocationMessage from {event.source.user_id} | Location : {event.message.latitude} {event.message.longitude}")
        reply_unregistration(event)

    return 200

@handler.add(MessageEvent, message=ImageMessage)
def handle_image_event(event):
    if(function_validate_registration_status(event)):
        print(f"\nImageMessage from {event.source.user_id} | Image : {event.timestamp}.jpg")
        if function_validate_key_json(event):
            function_save_image(event)
            function_append_image_json(event)
            reply_upload_images(event)
        else:
            reply_unalready_key_json(event)

    else:
        print(f"\nUnregistration User | ImageMessage from {event.source.user_id} | Image : {event.timestamp}")
        reply_unregistration(event)
    return 200

@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_event(event):
    if(function_validate_registration_status(event)):
        print(f"\nStickerMessage from {event.source.user_id} | StickerID : # PackageID : #")
    else:
        print(f"\nUnregistration User | StickerMessage from {event.source.user_id} | StickerID : # PackageID : #")
        reply_unregistration(event)
    return 200


if __name__ == '__main__':
    app.run(debug=True, port=8000)