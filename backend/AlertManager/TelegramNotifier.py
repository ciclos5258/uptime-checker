import requests

from pathlib import Path
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent   # папка, где лежит этот файл
ENV_PATH = BASE_DIR.parent.parent / ".env"
load_dotenv(ENV_PATH)
TOKEN = os.getenv("TOKEN")

def send_message(chat_id, text):
    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        json={
            "chat_id": chat_id,
            "text": text,
        },
        timeout=10
    )
def db_agent(cursor):
    cursor.execute("SELECT chat_id FROM users")

    for (chat_id,) in cursor.fetchall():
        send_message(chat_id, "🔴 Сайт недоступен")

