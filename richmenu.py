import os
import json
from linebot.models import RichMenu
from linebot import LineBotApi

line_bot_api = LineBotApi('ukIUk5jb/5/c8pwJ/ZfjM79eNK9YaEZ0VWQMf5GpmKmhqnWTXABLxZqJOlvdw8v0BZtKcfGC0URkSCK215UzJmyQFHJ6/rgnlb3Kp5Z0QG2SlPHoSZjWAf82YOh88ChSLPPfPWYuSMIoQ8M1r0W+4gdB04t89/1O/w1cDnyilFU=')

reply_root = ''
curr_path = os.getcwd()
rich_menu_folder = os.path.join(curr_path, 'material')  #要改路徑
rich_folders = os.listdir(rich_menu_folder)

for rich_menu in rich_folders:
    if rich_menu.startswith('rich_menu'):
        rich_menu_path = os.path.join(rich_menu_folder, rich_menu)
        if os.path.isdir(rich_menu_path):
            anything = os.listdir(rich_menu_path)
            file_path = ''
            jpg_path = ''
            for file in anything:
                if file == 'rich_menu.json':
                    file_path = os.path.join(rich_menu_path, file)
                elif file == 'rich_menu.jpg':
                    jpg_path = os.path.join(rich_menu_path, file)

        with open(file_path, 'r') as f:
            rich_menu_json = json.loads(f.read())

        # 創建菜單，取得menuId
        lineRichMenuId = line_bot_api.create_rich_menu(rich_menu=RichMenu.new_from_json_dict(rich_menu_json))
        print('設定檔上傳結果')
        print(lineRichMenuId)

        #id寫入指定資料夾端
        id_folder = os.path.join(rich_menu_path, 'rich_menu_id.txt')

        with open(id_folder, 'w') as rich_id:
            rich_id.write(lineRichMenuId)

        # 上傳照片至該menu-id
        with open(jpg_path, 'rb') as f:
           set_image_response = line_bot_api.set_rich_menu_image(lineRichMenuId, 'image/jpeg', f)
        print("-圖片上傳結果")
        print(set_image_response)

