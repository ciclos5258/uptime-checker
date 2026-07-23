import requests
from array import array

url_dict = {'homeclimatcontrol.ru': 'https://homeclimatcontrol.ru', 
            'red-hills-lab.ru': 'https://red-hills-lab.ru/', 
            'rendich76.ru': 'https://rendich76.ru'}

api_dict = {'homeclimatcontrol.ru': 'https://homeclimatcontrol.ru/api/latest'}

def health_check():

    # site access checking

    def status_code_checker(url):
        r = requests.get(url, timeout=10)
        return r.status_code

    for name, url in url_dict.items():
        status = status_code_checker(url)
        print(f"{name}: {status}")

# site apis checking
def api_check():
    def homeclimatcontrol_api_check(url):
        r = requests.get(url, timeout=10)
        return r.json()

    for name, url in api_dict.items():
        data_dict = homeclimatcontrol_api_check(url)
        success = data_dict['success']
        print(f"homeclimatcontrol.ru/api/latest access: {success}")

health_check()
api_check()