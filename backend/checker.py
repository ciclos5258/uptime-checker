import requests
import sqlite3
import logging
from datetime import datetime

# cfg
url_dict = {'homeclimatcontrol.ru': 'https://homeclimatcontrol.ru', 
            'red-hills-lab.ru': 'https://red-hills-lab.ru/', 
            'rendich76.ru': 'https://rendich76.ru'}

api_dict = {'homeclimatcontrol.ru': 'https://homeclimatcontrol.ru/api/latest'}

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='app.log'
)

def db_saver(cursor, url, status_code=None, api_answer=None):
    current_time = datetime.now().isoformat()
    try:
        cursor.execute(
            'INSERT INTO requests (timestamp, url, status_code, api_answer) VALUES (?,?,?,?)',
            (current_time, url, status_code, api_answer))
    except sqlite3.Error as e:
        logging.error(f"DB saving error. url: {url}, error: {e}", exec_info=True)

# site access checking4

def status_code_checker(url):
    try:
        r = requests.head(url, timeout=10)
        if r.status_code == 200:
            return r.status_code
        else:
            logging.warning(f"Unexpected status: {r.status_code} for {url}")
    except Exception as e:
        logging.error(f"HTTP request error. url: {url}, error: {e}", exec_info=True)

def homeclimatcontrol_api_check(url):
    try:
        r = requests.get(url, timeout=10)
        return r.json()
    except Exception as e:
        logging.error(f"API request error. url: {url}, error: {e}", exec_info=True)
def health_check(cursor):
    for name, url in url_dict.items():
        status_code = status_code_checker(url)
        print(f"{name}: {status_code}")
        db_saver(cursor, url, status_code)
        

# site apis checking
def api_check(cursor):
    for name, url in api_dict.items():
        data_dict = homeclimatcontrol_api_check(url)
        if data_dict is None:
            logging.error(f"API returned None for {url}")
            db_saver(cursor, url, api_answer=False)
        api_answer = data_dict['success']
        db_saver(cursor, url, api_answer=api_answer)
    print(f"homeclimatcontrol.ru/api/latest access: {api_answer}")

def check_should_alert(cursor, url, current_status):
    """
     func for sites status checking
    """
    cursor.execute(
        'SELECT status_code FROM requests WHERE url=? ORDER BY timestamp DESC LIMIT 2',
        (url,)
    )
    last_two = cursor.fetchall()
    
    if len(last_two) < 2:
        return False  # check history
    
    previous_status = last_two[1][0]
    
    was_ok = previous_status == 200
    is_ok = current_status == 200
    
    # Alert when status changed
    if was_ok and not is_ok:
        return "DOWN"  # the site is down
    elif not was_ok and is_ok:
        return "RECOVERED"  # the site is alive
    else:
        return False  # spam block