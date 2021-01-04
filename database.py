import csv, sqlite3

con = sqlite3.connect("ncufood.db")
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS food_table ('ResturantName', 'Kind','Holiday','Price','Location','OpenTime','Menu','FoodType');") # use your column names here

with open('菜單分類.csv','r') as fin: # `with` statement available in 2.5+
    #csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(fin) # comma is default delimiter
    to_db = [(i['\ufeffName'], i['找食物'],i['公休日'],i['平均價格'],i['店家位置'], i['營業時間'], i['菜單是否上傳'], i['食物風格']) for i in dr]

cur.executemany("INSERT INTO food_table ('ResturantName', 'Kind','Holiday','Price','Location','OpenTime','Menu','FoodType') VALUES (?,?,?,?,?,?,?,?);", to_db)
con.commit()

cur.execute('''select * from food_table ''')
print(cur.fetchall())
