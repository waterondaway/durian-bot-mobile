def function_greeting_template():
    template = {
        "type": "bubble",
        "hero": {
            "type": "image",
            "url": "https://github.com/waterondaway/durian-bot-mobile/blob/main/assets/static/banner_registration_to_access.png?raw=true",
            "size": "full",
            "aspectRatio": "18:6",
            "aspectMode": "cover",
            "action": {
            "type": "uri",
            "label": "Line",
            "uri": "https://linecorp.com/"
            }
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
                    "type": "separator"
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
                    "text": "ปล. โปรดกรอกข้อมูลให้ตรงกับรูปแบบที่ต้องการเพื่อประสิทธิภาพสูงสุด",
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
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "flex": 0,
            "spacing": "sm",
            "contents": [
            {
                "type": "button",
                "action": {
                "type": "message",
                "label": "ลงทะเบียนเข้าใช้งาน",
                "text": "ลงทะเบียนเข้าใช้งาน"
                },
                "color": "#4B524FFF",
                "height": "md",
                "style": "primary"
            }
            ]
        }
    }
    return template