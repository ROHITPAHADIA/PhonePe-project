import sqlite3

DB_FILE = "db/phonepe_data.db"

def get_connection():
    return sqlite3.connect(DB_FILE)
