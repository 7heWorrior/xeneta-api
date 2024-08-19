import psycopg2
from psycopg2 import pool
import os

DATABASE_URI = os.getenv('DATABASE')


connection_pool = None

def init_connection_pool(minconn=1, maxconn=10):
    global connection_pool
    connection_pool = psycopg2.pool.SimpleConnectionPool(minconn, maxconn, DATABASE_URI)

def get_db_connection():
    """
    Returns a database connection from the pool.
    """
    if connection_pool:
        return connection_pool.getconn()
    else:
        # Fall back to a single connection if no pool is used
        return psycopg2.connect(DATABASE_URI)

def release_db_connection(conn):
    """
    Releases the database connection back to the pool.
    """
    if connection_pool:
        connection_pool.putconn(conn)
    else:
        conn.close()
