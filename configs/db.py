import os
import psycopg2

DATABASE_URI = os.getenv('DATABASE')

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URI)
    return conn
