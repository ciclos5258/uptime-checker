import requests
import sqlite3
from datetime import datetime

# cfg
url_dict = {'homeclimatcontrol.ru': 'https://homeclimatcontrol.ru', 
            'red-hills-lab.ru': 'https://red-hills-lab.ru/', 
            'rendich76.ru': 'https://rendich76.ru'}

api_dict = {'homeclimatcontrol.ru': 'https://homeclimatcontrol.ru/api/latest'}

#DB init

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
def db_saver(url, status_code=None, api_answer=None):
    current_time = datetime.now().isoformat()
    cursor.execute(
        'INSERT INTO requests (timestamp, url, status_code, api_answer) VALUES (?,?,?,?)',
        (current_time, url, status_code, api_answer)
        )

# site access checking4

def status_code_checker(url):
    r = requests.get(url, timeout=10)
    return r.status_code

def homeclimatcontrol_api_check(url):
    r = requests.get(url, timeout=10)
    return r.json()

def health_check():
    for name, url in url_dict.items():
        status_code = status_code_checker(url)
        print(f"{name}: {status_code}")
        db_saver(url, status_code)
        

# site apis checking
def api_check():
    for name, url in api_dict.items():
        data_dict = homeclimatcontrol_api_check(url)
        api_answer = data_dict['success']
        db_saver(url, api_answer=api_answer)
    print(f"homeclimatcontrol.ru/api/latest access: {api_answer}")

health_check()
api_check()

connection.commit()
cursor.close()
connection.close()