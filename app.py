from flask import Flask, request, abort

from linebot import (
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
import copy
from linebot.models import RichMenu
import psycopg2

app = Flask(__name__)
line_bot_api = LineBotApi('xxxxxxx')
handler = WebhookHandler('xxxxxxx')


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
    # open material file to transform to json
    reply_root = ''  # final location
    reply_path = ''  # dir
    curr_path = os.getcwd()
    Textreply_folder = os.path.join(curr_path, 'material')
    reply_folders = os.listdir(Textreply_folder)
    for folder in reply_folders:
        if folder == fileName:
            reply_path = os.path.join(Textreply_folder, folder)
        else:
            #如果沒有在material資料夾，就用英文機器人回覆
            return []
            break

    #開啟material資料夾後的解析json
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
@handler.add(FollowEvent)
def process_follow_event(event):
    reply_arr = []
    replyJsonPath = 'Follow'
    reply_arr = detect_from_follower(replyJsonPath)

    # 消息發送
    line_bot_api.reply_message(
        event.reply_token,
        reply_arr
    )

from chatbot import chat
# 處理文字訊息
@handler.add(MessageEvent, message=TextMessage)
def process_text_message(event):
    replyJsonPath = event.message.text
    if detect_from_follower(replyJsonPath):
        message_array = detect_from_follower(replyJsonPath)
        line_bot_api.reply_message(event.reply_token, message_array)
    else:
        message_array = chat(replyJsonPath)
        print(message_array)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(message_array))

# 用戶發PostbackEvent時，若指定menu=xxx，則可更換menu
# 若menu欄位有值，則：
# 讀取其rich_menu_id，並取得用戶id，將用戶與選單綁定
# 讀取其reply.json，轉譯成消息，並發送
from insert_context_postgre import insert_user_data
from search_food_postgre import search_data_query
from create_carousel import carousel_food
from random_food import random_search

@handler.add(PostbackEvent)
def process_postback_event(event):
    query_string_dict = parse_qs(event.postback.data)
    print(query_string_dict)

    print(event.source.user_id)
    if 'FoodType' in query_string_dict:
        FoodType_postback = query_string_dict.get('FoodType')[0]
        insert_user_data('FoodType', FoodType_postback, event.source.user_id)
        print('good')

    if 'Price' in query_string_dict:
        Price_postback = query_string_dict.get('Price')[0]
        insert_user_data('Price', Price_postback, event.source.user_id)
        print('okkk')

    if 'Location' in query_string_dict:
        Location_postback = query_string_dict.get('Location')[0]
        insert_user_data('Location', Location_postback, event.source.user_id)

    if 'OpenTime' in query_string_dict:
        OpenTime_postback = query_string_dict.get('OpenTime')[0]
        insert_user_data('OpenTime', OpenTime_postback, event.source.user_id)

    if 'Kind' in query_string_dict:
        Kind_postback = query_string_dict.get('Kind')[0]
        insert_user_data('Kind', Kind_postback, event.source.user_id)

    if 'check' in query_string_dict:
        check_postback = query_string_dict.get('check')[0]
        if check_postback == 'Checkdata':
            message_array = detect_from_follower(check_postback)
            line_bot_api.reply_message(event.reply_token, message_array)

    if 'query' in query_string_dict:
        query_postback = query_string_dict.get('query')[0]
        if query_postback == 'yes':
            results = search_data_query(event.source.user_id)
            if results:
                #carousel template
                template_carousel = {
                                    "type": "flex",
                                    "altText": "You have a new message!",
                                    "contents": {
                                        "type": "carousel",
                                        "contents": []
                                    }
                }

                for shop in results:
                    name = shop[0]
                    #print(name)
                    message_array = carousel_food(name)
                    #print(message_array)
                    #print('-'*30)
                    temp = copy.deepcopy(message_array)
                    template_carousel['contents']['contents'].append(temp)
                message_array = FlexSendMessage.new_from_json_dict(template_carousel)
                #print(message_array)
                line_bot_api.reply_message(event.reply_token, message_array)
            else:
                results = 'no_results'
                message_array = detect_from_follower(results)
                line_bot_api.reply_message(event.reply_token, message_array)

    if 'action' in query_string_dict:
        query_action = query_string_dict.get('action')[0]
        if query_action == 'feedback':
            message_array = detect_from_follower(query_action)
            line_bot_api.reply_message(event.reply_token, message_array)
        if query_action == 'random':
            number = 5
            results = random_search(number)
            template_carousel = {
                "type": "flex",
                "altText": "You have a new message!",
                "contents": {
                    "type": "carousel",
                    "contents": []
                }
            }

            for shop in results:
                name = shop[0]
                # print(name)
                message_array = carousel_food(name)
                # print(message_array)
                # print('-'*30)
                temp = copy.deepcopy(message_array)
                template_carousel['contents']['contents'].append(temp)
            message_array = FlexSendMessage.new_from_json_dict(template_carousel)
            # print(message_array)
            line_bot_api.reply_message(event.reply_token, message_array)

    print('--------------check----------------')
    if 'menu' in query_string_dict:
        replyJsonPath = query_string_dict.get('menu')[0]  # 'rich_menu_2'
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
