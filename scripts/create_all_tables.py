from db_utils import get_connection

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS aggregated_transaction (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        year INTEGER,
        quarter INTEGER,
        state TEXT,
        transaction_type TEXT,
        count INTEGER,
        amount REAL
    );

    CREATE TABLE IF NOT EXISTS aggregated_user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        year INTEGER,
        quarter INTEGER,
        state TEXT,
        brand TEXT,
        count INTEGER,
        percentage REAL
    );

    CREATE TABLE IF NOT EXISTS aggregated_insurance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        year INTEGER,
        quarter INTEGER,
        state TEXT,
        count INTEGER,
        amount REAL
    );

    CREATE TABLE IF NOT EXISTS map_user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        year INTEGER,
        quarter INTEGER,
        state TEXT,
        district TEXT,
        registered_users INTEGER,
        app_opens INTEGER
    );
    """)

    conn.commit()
    conn.close()
    print("✅ All tables created successfully.")

if __name__ == "__main__":
    create_tables()
