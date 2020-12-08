import os
from linebot import(
    LineBotApi
)
import json

line_bot_api = LineBotApi("YOUR_CHANNEL_ACCESS_TOKEN")

print(line_bot_api.get_rich_menu_list())
