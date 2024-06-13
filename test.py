import os
import mysql.connector
from mysql.connector import Error

try:
    conn = mysql.connector.connect(
        host='localhost',
        database='youtube_comments_db',
        username='root',
        password=os.getenv("PASSWORD")
    )
    if conn.is_connected():
        print('Connected to MySQL database')
        cursor = conn.cursor()

except Error as e:
    print(f"Error:{e}")
