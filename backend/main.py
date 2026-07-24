from checker import health_check, api_check, sqlite3

def db_init():
    connection = sqlite3.connect('requests.db')
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS requests(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    url TEXT NOT NULL,
    status_code INTEGER,
    api_answer TEXT
    )
    ''')
    
    return connection, cursor

connection, cursor = db_init()

health_check(cursor)
api_check(cursor)

connection.commit()

cursor.close()
connection.close()