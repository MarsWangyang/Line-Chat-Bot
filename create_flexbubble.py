import os
import json
import psycopg2


DATABASE_URL = os.popen('heroku config:get DATABASE_URL -a ncu-food').read()[:-1]
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cursor = conn.cursor()

search_query = """SELECT * FROM food"""
cursor.execute(search_query)
user_data = cursor.fetchall()
#print(user_data)
template_bubble = {
  "type": "bubble",
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "Brown Cafe",  #店名['body']['contents'][0]['text']
        "weight": "bold",
        "size": "xl"
      },
      {
        "type": "box",
        "layout": "vertical",
        "margin": "lg",
        "spacing": "sm",
        "contents": [     #['body']['contents'][1]['contents']
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "Place",     #['body']['contents'][1]['contents'][0]['contents'][0]['text']
                "color": "#aaaaaa",
                "size": "sm",
                "flex": 1
              },
              {
                "type": "text",
                "text": "Miraina Tower, 4-1-6 Shinjuku, Tokyo",   #['body']['contents'][1]['contents'][0]['contents'][1]['text']
                "wrap": True,
                "color": "#666666",
                "size": "sm",
                "flex": 5
              }
            ]
          },
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "Time",     #['body']['contents'][1]['contents'][1]['contents'][0]['text']
                "color": "#aaaaaa",
                "size": "sm",
                "flex": 1
              },
              {
                "type": "text",
                "text": "10:00 - 23:00",  #['body']['contents'][1]['contents'][1]['contents'][1]['text']
                "wrap": True,
                "color": "#666666",
                "size": "sm",
                "flex": 5
              }
            ]
          },
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "Type",     #['body']['contents'][1]['contents'][2]['contents'][0]['text']
                "color": "#aaaaaa",
                "size": "sm",
                "flex": 1
              },
              {
                "type": "text",
                "text": "10:00 - 23:00",  #['body']['contents'][1]['contents'][2]['contents'][1]['text']
                "wrap": True,
                "color": "#666666",
                "size": "sm",
                "flex": 5
              }
            ]
          }
        ]
      }
    ]
  },
}



# template_type = {
#     "type": "flex",
#     "contents": template_bubble
#}

path = './material/'
for shop in user_data[:-1]:
    name = shop[0]
    eatordrink = shop[1]
    holiday = shop[2]
    price = shop[3]
    location = shop[4]
    opentime = shop[5]
    menu = shop[6]
    foodtype = shop[7]
    template_bubble['body']['contents'][0]['text'] = name
    template_bubble['body']['contents'][1]['contents'][0]['contents'][1]['text'] = location
    template_bubble['body']['contents'][1]['contents'][1]['contents'][1]['text'] = opentime
    template_bubble['body']['contents'][1]['contents'][2]['contents'][1]['text'] = foodtype
    print('template updated!')
    try:
        os.mkdir(path + name)
        print('建立資料夾')
    except:
        print('資料夾已經存在')

    with open(path+name+'/reply.json', 'w') as f:
        json.dump(template_bubble, f)
        print('資料已上傳')
    print('-' * 20)