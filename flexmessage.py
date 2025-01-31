def function_greeting_template():
    template = {
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
                    "type": "separator"
                },
                {
                    "type": "text",
                    "text": "1. กดปุ่ม `ลงทะเบียนเข้าใช้งาน` \n2. ดำเนินการกรอกข้อมูลดังต่อไปนี้ : \nชื่อ-นามสกุล, เบอร์โทรติดต่อ, รหัสเกษตรกร, สังกัดจังหวัด",
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

def function_user_information_template():
    template = {
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
                "text": "ชื่อ-นามสกุล :",
                "weight": "regular",
                "align": "start",
                "margin": "md",
                "wrap": True,
                "contents": []
              },
              {
                "type": "text",
                "text": "เบอร์โทรติดต่อ :",
                "weight": "regular",
                "align": "start",
                "margin": "md",
                "wrap": True,
                "contents": []
              },
              {
                "type": "text",
                "text": "รหัสเกษตรกร :",
                "weight": "regular",
                "align": "start",
                "margin": "md",
                "wrap": True,
                "contents": []
              },
              {
                "type": "text",
                "text": "สังกัดจังหวัด :",
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
                "text": "ตัวอย่างการป้อนข้อมูล : \nสมชาย ใจดี\n0999999999\n581-123-941-239\nกรุงเทพมหานคร",
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
    return template
  
def function_user_registration_complete_template(farmer_name, telephone, farmer_id, organization):
    template = {
      "type": "bubble",
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
                "text": f"ชื่อ-นามสกุล : {farmer_name}",
                "weight": "regular",
                "align": "start",
                "margin": "md",
                "wrap": True,
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
                "text": f"รหัสเกษตรกร : {farmer_id}",
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
            ]
          }
        ]
      }
    }
    return template