import json
import requests
from flask import *
#with open('config.json', 'r') as config_file:
#    config = json.load(config_file)

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


class LiveConnection():
    def __init__(self,ip,port):
        self.ip = ip
        self.port = port
        self.url_prefix = "http://" + str(ip) + ":" + str(port) 
        self.headers,self.cookies = initialize_connection()
        self.token = None 
        self.jwt = None
     
    def initialize_connection():
        r = requests.get(self.url_prefix+'/status/', timeout=2.50)
        return r.cookies,r.headers

    # ------ FHE ROUTES ------
    def get_set(self,set_id):
        body = {"set_id":str(set_id)}
        headers = self.headers["Authorization"] = str(self.jwt)
        r = requests.get(data=body,self.url_prefix+"/integers/set/",headers=headers,cookies=self.cookies, timeout=2.50)
        return r.text

    def post_set(self,integers):
        r = requests.post(self.url_prefix+'/integers/set/', timeout=2.50)
        return r.text

    def del_set(self,set_id):        
        r = requests.delete(self.url_prefix+'/integers/set/', timeout=2.50)
        return r.text

    def post_operation(self,operation):
        body = {"equation":str(operation)}
        r = requests.post(data=body,self.url_prefix+'/integers/operation/', timeout=2.50)
        return r.text 

    def get_session(self,session_id):
        r = requests.get(self.url_prefix+"/integers/session/", timeout=2.50)
        return r.text

    def post_session(self):
        r = requests.post(self.url_prefix+"/integers/session/", timeout=2.50)
        return r.text

    def del_session(self):
        r = requests.delete(self.url_prefix+"/integers/session/", timeout=2.50)
        return r.text

    # ------ API/AUTH ROUTES ------
    def get_status(self): 
        r = requests.get(self.url_prefix+'/status/', timeout=2.50)
        return r.text

    def get_jwt(self,token):
        headers = {"Authorization":"Token "+str(token)}
        r = requests.get(self.url_prefix+'/api/jwt/', timeout=2.50)
        return r.text

    def post_refresh(self,jwt):
        headers = {"Authorization":"Bearer "+str(token)} # include in header or body? 
        r = requests.post(self.url_prefix+'/api/jwt/refresh/', timeout=2.50)
        return r.text

    def post_verify(self,jwt):
        #headers = {"Authorization":"Token "+str(token)} # where to include access token?
        r = requests.post(self.url_prefix+'/api/jwt/verify/', timeout=2.50)
        return r.text

    def post_signup(self,form_data): 
        if self.token not None:
            raise AttributeError
        else:
            r = requests.post(self.url_prefix+'/api/auth/signup/', timeout=2.50)
            self.token = json.loads(r.content.decode('utf8').replace("'", '"'))["deviceToken"]
            return self.token

    def post_login(self,form_data):
        r = requests.post(self.url_prefix+'/api/auth/login/', timeout=2.50,  files=dict(form_data)) # files is used to send form-data
        return r.text

    def post_logout(self,jwt):
        headers = {"Authorization":"Bearer " + str(jwt)}
        r = requests.post(self.url_prefix+'/api/auth/logout/', timeout=2.50,  files=dict(form_data)) # files is used to send form-data
        return r.text

    def post_del_logout(self,jwt): # USE CAUTIOUSLY, WILL DELETE ALL DATA TIED TO SESSION ENSURE DOWNLOADED
        headers = {"Authorization":"Bearer " + str(jwt)}
        r = requests.post(self.url_prefix+'/api/auth/del-logout/', timeout=2.50,  files=dict(form_data)) # files is used to send form-data
        return r.text

