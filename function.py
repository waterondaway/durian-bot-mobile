def func_registration_to_access():
    return {
    "type": "bubble",
    "hero": {
        "type": "image",
        "url": "https://github.com/waterondaway/durian-bot-mobile/blob/main/assets/static/banner_registration_to_access.png?raw=true",
        "size": "full",
        "aspectRatio": "18:6",
        "aspectMode": "cover",
    },
    "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
        {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "ขั้นตอนการลงทะเบียนเข้าใช้งาน",
                "weight": "bold",
                "align": "start",
                "contents": []
            },
            {
                "type": "separator",
                "margin": "md"
            },
            {
                "type": "text",
                "text": "1. กดปุ่ม `ลงทะเบียนเข้าใช้งาน` \n2. ดำเนินการกรอกข้อมูลดังต่อไปนี้ : \nชื่อ-นามสกุล, เบอร์มือถือ, สังกัดจังหวัด\n3. กดปุ่ม `ยืนยันการลงทะเบียน`",
                "weight": "regular",
                "align": "start",
                "margin": "md",
                "wrap": True,
                "contents": []
            },
            {
                "type": "text",
                "text": "ปล. หากต้องการแก้ไขข้อมูล กดปุ่ม `ละทิ้ง` เพื่อกรอกข้อมูลใหม่อีกครั้ง",
                "weight": "bold",
                "size": "sm",
                "color": "#AAAAAAFF",
                "margin": "md",
                "wrap": True,
                "contents": []
            }
            ]
        }
        ]
    }
    }

def func_registration_data_collection_form(fullname='',telephone='',organization=''):
    return {
    "type": "bubble",
    "hero": {
        "type": "image",
        "url": "https://github.com/waterondaway/durian-bot-mobile/blob/main/assets/static/banner_user_account_information.png?raw=true",
        "size": "full",
        "aspectRatio": "18:6",
        "aspectMode": "cover"
    },
    "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
        {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "ข้อมูลการลงทะเบียนเข้าใช้งาน",
                "weight": "bold",
                "align": "start",
                "contents": []
            },
            {
                "type": "separator",
                "margin": "md"
            },
            {
                "type": "text",
                "text": f"ชื่อ-นามสกุล : {fullname}",
                "weight": "regular",
                "align": "start",
                "margin": "md",
                "wrap": False,
                "contents": []
            },
            {
                "type": "text",
                "text": f"เบอร์โทรติดต่อ : {telephone}",
                "weight": "regular",
                "align": "start",
                "margin": "md",
                "wrap": True,
                "contents": []
            },
            {
                "type": "text",
                "text": f"สังกัดจังหวัด : {organization}",
                "weight": "regular",
                "align": "start",
                "margin": "md",
                "wrap": True,
                "contents": []
            },
            {
                "type": "separator",
                "margin": "md"
            },
            {
                "type": "text",
                "text": "ตัวอย่างการป้อนข้อมูล : \nสมชาย ใจดี\n0999999999\nกรุงเทพมหานคร",
                "weight": "bold",
                "size": "sm",
                "color": "#AAAAAAFF",
                "margin": "md",
                "wrap": True,
                "contents": []
            },
            {
                "type": "text",
                "text": "ปล. หากต้องการแก้ไขข้อมูล กดปุ่ม `ละทิ้ง` เพื่อกรอกข้อมูลใหม่อีกครั้ง",
                "weight": "bold",
                "size": "sm",
                "color": "#AAAAAAFF",
                "margin": "md",
                "wrap": True,
                "contents": []
            }
            ]
        }
        ]
    }
    }