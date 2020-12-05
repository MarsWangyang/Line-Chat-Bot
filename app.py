from flask import Flask, request, abort

from linebot import(
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
from linebot.models.template import *
import json

from linebot.models import (
    PostbackEvent
)
from urllib.parse import parse_qs
from linebot.models import RichMenu

app = Flask(__name__)

line_bot_api = LineBotApi('ukIUk5jb/5/c8pwJ/ZfjM79eNK9YaEZ0VWQMf5GpmKmhqnWTXABLxZqJOlvdw8v0BZtKcfGC0URkSCK215UzJmyQFHJ6/rgnlb3Kp5Z0QG2SlPHoSZjWAf82YOh88ChSLPPfPWYuSMIoQ8M1r0W+4gdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('d077ff15d7b1005f7778d8175a6e4df9')


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

def detect_from_follower(fileName):

    #open material file to transform to json
    reply_root = '' #final location
    reply_path = '' #dir
    curr_path = os.getcwd()
    Textreply_folder = os.path.join(curr_path, 'material')
    reply_folders = os.listdir(Textreply_folder)
    for folder in reply_folders:
        if folder == fileName:
            reply_path = os.path.join(Textreply_folder, folder)
    for file in os.listdir(reply_path):
        if file == 'reply.json':
            reply_root = os.path.join(reply_path, file)

    with open(reply_root) as f:
        json_arr = json.loads(f.read())

    returnArr = []
    message_type = json_arr.get('type')
    # 轉換
    if message_type == 'text':
        returnArr.append(TextSendMessage.new_from_json_dict(json_arr))
    elif message_type == 'imagemap':
        returnArr.append(ImagemapSendMessage.new_from_json_dict(json_arr))
    elif message_type == 'template':
        returnArr.append(TemplateSendMessage.new_from_json_dict(json_arr))
    elif message_type == 'image':
        returnArr.append(ImageSendMessage.new_from_json_dict(json_arr))
    elif message_type == 'sticker':
        returnArr.append(StickerSendMessage.new_from_json_dict(json_arr))
    elif message_type == 'audio':
        returnArr.append(AudioSendMessage.new_from_json_dict(json_arr))
    elif message_type == 'location':
        returnArr.append(LocationSendMessage.new_from_json_dict(json_arr))
    elif message_type == 'flex':
        returnArr.append(FlexSendMessage.new_from_json_dict(json_arr))
    elif message_type == 'video':
        returnArr.append(VideoSendMessage.new_from_json_dict(json_arr))
    return returnArr


# 處理關注
#@handler.add(FollowEvent)
#def process_follow_event(event):
#    return 0


# 處理文字訊息
@handler.add(MessageEvent, message=TextMessage)
def process_text_message(event):
    replyJsonPath = event.message.text
    message_array = detect_from_follower(replyJsonPath)
    line_bot_api.reply_message(event.reply_token, message_array)

#用戶發PostbackEvent時，若指定menu=xxx，則可更換menu
#若menu欄位有值，則：
#讀取其rich_menu_id，並取得用戶id，將用戶與選單綁定
#讀取其reply.json，轉譯成消息，並發送

@handler.add(PostbackEvent)
def process_postback_event(event):
    query_string_dict = parse_qs(event.postback.data)
    print(query_string_dict)

    if 'menu' in query_string_dict:
        replyJsonPath = query_string_dict.get('menu')[0]  #'rich_menu_2'
        linkRichMenuId = query_string_dict.get('menu')[0]

        # 開啟檔案，轉成json
        curr_path = os.getcwd()
        rich_menu_folder = os.path.join(curr_path, 'material')
        rich_folders = os.listdir(rich_menu_folder)
        linkRichMenuId_path = ''

        for rich_menu in rich_folders:
            if rich_menu == linkRichMenuId:
                rich_menu_path = os.path.join(rich_menu_folder, rich_menu)
                anything = os.listdir(rich_menu_path)
                for file in anything:
                    if file == 'rich_menu_id.txt':
                        linkRichMenuId_path = os.path.join(rich_menu_path, 'rich_menu_id.txt')
                        break

        with open(linkRichMenuId_path, 'r') as f:
            linkRichMenuId = f.readline()
        print(linkRichMenuId)
        print(replyJsonPath)
        # 綁定圖文選單
        line_bot_api.link_rich_menu_to_user(event.source.user_id, linkRichMenuId)

        result_message_array = detect_from_follower(replyJsonPath)
        line_bot_api.reply_message(
            event.reply_token,
            result_message_array
        )

    elif 'folder' in query_string_dict:
        replyJsonPath = query_string_dict.get('folder')[0]

        result_message_array = detect_from_follower(replyJsonPath)
        line_bot_api.reply_message(
            event.reply_token,
            result_message_array
        )


import os
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
