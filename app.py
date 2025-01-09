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
    MessageEvent, FollowEvent, TextMessage
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
    return

if __name__ == '__main__':
    app.run(debug=True, port=5000)