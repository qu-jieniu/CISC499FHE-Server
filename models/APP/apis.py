import requests
import json

def connect_server(ip, port):
    url = 'http://' + str(ip) + ":" + str(port)
    payload = {'uuid':10086}
    r = requests.post(url, data=json.dumps(payload), timeout=2.50)
    # ... Todo on returned get
    return True

def check_exist_session(ip, port, name):
    url = 'http://' + str(ip) + ":" + str(port)
    public_ip = requests.get('https://api.ipify.org').text
    # ... Todo on returned get
    return False
