from app import *
from externalLib import *

headers = {"Content-type":'application/json', "Authorization": None}

def connect_server(ip, port):
    url = 'http://' + str(ip) + ":" + str(port) + "/status/"
    r = requests.get(url, timeout=2.50)
    if r.status_code == 200:
        return True
    else:
        return False

def create_session():
    url_prefix = 'http://' + str(session['ip']) + ":" + str(session['port'])
    uuid0 = uuid.uuid4()
    password = os.urandom(8)
    # SIGNUP
    body = {'username': str(uuid0), 'password1': str(password), 'password2': str(password)}
    r = requests.post(url_prefix + "/api/auth/signup/" , data=body)
    session['device-token'] = r.json()["token"]
    session['django-cookie'] = r.cookies.get_dict()
    # GET JWT PAIR
    headers['Authorization'] = "Token " + session['device-token']
    r = requests.get(url_prefix + '/api/jwt/', headers=headers, timeout=2.50)
    session['access-token'] = r.json()['access']
    session['refresh-token'] = r.json()['refresh']
    session['server_id'] = session['django-cookie']['sessionid']
    headers['Authorization'] = "Bearer " + session['access-token']

def create_data(x0, p0):
    url_prefix = 'http://' + str(session['ip']) + ":" + str(session['port'])
    headers['Authorization'] = "Bearer " + session['access-token']
    body= {"integers":[{"index":0, "X":x0, "q":p0}]}
    r = requests.post(url_prefix + '/integers/set/', json=body, headers=headers, cookies=session['django-cookie'], timeout=2.50)
    return r.json()['set_id']

def create_eval(id_str):
    url_prefix = 'http://' + str(session['ip']) + ":" + str(session['port'])
    headers['Authorization'] = "Bearer " + session['access-token']
    body= {"equation": str(id_str)}
    r = requests.post(url_prefix + '/integers/operation/', json=body, headers=headers, cookies=session['django-cookie'], timeout=2.50)
    return r.json()['setCreated']

def get_x_prime(id):
    url_prefix = 'http://' + str(session['ip']) + ":" + str(session['port'])
    headers['Authorization'] = "Bearer " + session['access-token']
    body = {"set_id": id}
    r = requests.get(url_prefix + '/integers/set/', json=body, headers=headers, cookies=session['django-cookie'], timeout=2.50)
    return r.json()['integers'][0].get("X")


class LiveConnection():
    def __init__(self,ip,port,url=None):
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
        r = requests.get(self.url_prefix+"/integers/set/", data=body, headers=headers,cookies=self.cookies, timeout=2.50)
        return r.text

    def post_set(self,integers):
        r = requests.post(self.url_prefix+'/integers/set/', timeout=2.50)
        return r.text

    def del_set(self,set_id):
        r = requests.delete(self.url_prefix+'/integers/set/', timeout=2.50)
        return r.text

    def post_operation(self,operation):
        body = {"equation":str(operation)}
        r = requests.post(self.url_prefix+'/integers/operation/', data=body, timeout=2.50)
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
        if self.token is not None:
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
