import json
import requests
from flask import *

def connect_server(ip, port):
    # url = 'http://' + str(session['ip']) + ":" + str(session['port']) + "/admin/"
    url = 'http://' + str(ip) + ":" + str(port)
    r = requests.get(url, timeout=2.50)
    if r.status_code == 200:
        return True
    else:
        return False

def exist_session(session_name):
    # ... Todo on returned get
    return False

def create_data(label, xp_add, xp_mul):
    return '1234567890'

def create_eval(id_str):
    return '1234567890'

def decrypt(id):
    return 1938
