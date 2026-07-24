import requests
import sqlite3
from datetime import datetime
from array import array
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


def health_check():

    # site access checking

    def status_code_checker(url):
        r = requests.get(url, timeout=10)
        return r.status_code

    for name, url in url_dict.items():
        status = status_code_checker(url)
        print(f"{name}: {status}")
        current_time = datetime.now().isoformat()
        cursor.execute(
            'INSERT INTO requests (timestamp, url, status_code) VALUES (?,?,?)',
            (current_time, url, status)
        )

    connection.commit()

# site apis checking
def api_check():
    def homeclimatcontrol_api_check(url):
        r = requests.get(url, timeout=10)
        return r.json()

    for name, url in api_dict.items():
        data_dict = homeclimatcontrol_api_check(url)
        success = data_dict['success']
        current_time = datetime.now().isoformat()
        cursor.execute(
            'INSERT INTO requests (timestamp, url, api_answer) VALUES (?,?,?)',
            (current_time, url, success)
        )
    connection.commit()
    print(f"homeclimatcontrol.ru/api/latest access: {success}")

health_check()
api_check()

cursor.close()
connection.close()