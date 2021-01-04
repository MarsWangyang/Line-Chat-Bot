import os
import psycopg2

def random_search(number):
    DATABASE_URL = os.environ['DATABASE_URL']
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()

    search_query = """SELECT * FROM food ORDER BY RANDOM() LIMIT %s"""
    cursor.execute(search_query, (number, ))
    results = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    return results