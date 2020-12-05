import os
from linebot import(
    LineBotApi
)
import json

line_bot_api = LineBotApi("ukIUk5jb/5/c8pwJ/ZfjM79eNK9YaEZ0VWQMf5GpmKmhqnWTXABLxZqJOlvdw8v0BZtKcfGC0URkSCK215UzJmyQFHJ6/rgnlb3Kp5Z0QG2SlPHoSZjWAf82YOh88ChSLPPfPWYuSMIoQ8M1r0W+4gdB04t89/1O/w1cDnyilFU=")
line_bot_api.delete_rich_menu("richmenu-b7355771378483d3ad3d564cb68d46d5")
line_bot_api.delete_rich_menu("richmenu-eae3f2e23a396336e365b4d129d332b5")
#line_bot_api.delete_rich_menu("richmenu-3c424d42f70ede0c26f1e5fb0ff476a4")
#line_bot_api.delete_rich_menu("richmenu-bad7578cd49c63727a95b41645c4b038")
print(line_bot_api.get_rich_menu_list())
