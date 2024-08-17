import psycopg2
from os import getenv
# Database configuration
DATABASE_URI = getenv('DATABASE')

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URI)
    return conn
