import os
import psycopg2

def search_data_query(user_id):
    DATABASE_URL = os.environ['DATABASE_URL']

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()

    search_query = """SELECT * FROM context WHERE Id=%s"""
    cursor.execute(search_query, (user_id,))
    user_data = cursor.fetchall()[0]
    print(user_data)
    print('----------')


    search_query = """SELECT * FROM food
                      WHERE (Price=%s AND
                            string_to_array(Location,',') @> array[%s] AND 
                            string_to_array(OpenTime,',') @> array[%s] AND 
                            string_to_array(FoodType,',') @> array[%s])"""

    cursor.execute(search_query, (user_data[1], user_data[2], user_data[3], user_data[4]))
    result = cursor.fetchall()
    print("Result:", result)

    conn.commit()
    cursor.close()
    conn.close()
    return result
