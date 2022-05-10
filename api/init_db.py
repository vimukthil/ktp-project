import sqlite3

def connect_to_db():
    conn = sqlite3.connect('ktp.db')
    return conn


def create_db_table():
    try:
        conn = connect_to_db()
        conn.execute('''DROP TABLE IF EXISTS items''')
        conn.execute('''
            CREATE TABLE items (
                id INTEGER PRIMARY KEY NOT NULL,
                name TEXT NOT NULL,
                price INTEGER NOT NULL,
                quantity INTEGER NOT NULL
            );
        ''')

        conn.commit()
        print("Item table created successfully")
    except:
        print("Item table creation failed")
    finally:
        conn.close()
