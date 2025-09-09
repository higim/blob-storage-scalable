import os

import psycopg2

DB_URL = os.getenv("DATABASE_URL")

def get_connection():
    return psycopg2.connect(DB_URL)

def save_file_metadata(filename: str, status: str = "pending"):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS files (
                id SERIAL PRIMARY KEY,
                filename TEXT,
                status TEXT,
                created_at TIMESTAMP DEFAULT NOW()
        )            
    """)
    cur.execute("INSERT INTO files (filename, status) VALUES (%s, %s)", (filename, status))
    conn.commit()
    cur.close()
    conn.close()
