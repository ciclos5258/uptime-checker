import logging

from pathlib import Path
from checker import health_check, api_check, check_should_alert, sqlite3
from AlertManager.TelegramNotifier import send_message

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='app.log'
)

def db_init():
    # Используем абсолютный путь к БД в папке backend
    db_path = Path(__file__).resolve().parent / "requests.db"
    connection = sqlite3.connect(db_path)
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

    ('''CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id INTEGER PRIMARY KEY,
    username TEXT,
    first_name TEXT,
    subscribed INTEGER DEFAULT 1
    )
    ''');
    
    return connection, cursor

connection, cursor = db_init()

health_check(cursor)
api_check(cursor)

connection.commit()

if check_should_alert() == "DOWN":
    try:
        send_message()
    except:
        logging.error(f"Sending message error")

cursor.close()
connection.close()