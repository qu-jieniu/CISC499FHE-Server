from app import *
from externalLib import *

headers = {"Content-type":'application/json', "Authorization": None}

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
    session['server_id'] = session['django-cookie']['sessionid']

def create_data(x0, q0):
    url_prefix = 'http://' + str(session['ip']) + ":" + str(session['port'])
    headers['Authorization'] = "Token " + session['device-token']
    r = requests.get(url_prefix + '/api/jwt/', headers=headers, timeout=2.50)
    session['access-token'] = r.json()['access']

    headers['Authorization'] = "Bearer " + session['access-token']
    x0_e = base64.b64encode(x0.to_bytes(math.ceil(x0.bit_length()/8),'big')).decode()
    q0_e = base64.b64encode(q0.to_bytes(math.ceil(q0.bit_length()/8),'big')).decode()
    print(x0, x0_e)
    body= {"integers":[{"index":0, "X":str(x0_e), "q":str(q0_e)}]}
    r = requests.post(url_prefix + '/integers/set/', json=body, headers=headers, cookies=session['django-cookie'], timeout=2.50)
    return r.json()['set_id']

def create_eval(id_str):
    url_prefix = 'http://' + str(session['ip']) + ":" + str(session['port'])
    headers['Authorization'] = "Token " + session['device-token']
    r = requests.get(url_prefix + '/api/jwt/', headers=headers, timeout=2.50)
    session['access-token'] = r.json()['access']

    headers['Authorization'] = "Bearer " + session['access-token']
    body= {"equation": str(id_str)}
    r = requests.post(url_prefix + '/integers/operation/', json=body, headers=headers, cookies=session['django-cookie'], timeout=2.50)
    print(r.text)
    return r.json()['setCreated']

def get_encrypted(id):
    url_prefix = 'http://' + str(session['ip']) + ":" + str(session['port'])
    headers['Authorization'] = "Token " + session['device-token']
    r = requests.get(url_prefix + '/api/jwt/', headers=headers, timeout=2.50)
    session['access-token'] = r.json()['access']

    headers['Authorization'] = "Bearer " + session['access-token']
    body = {"set_id": id}
    r = requests.get(url_prefix + '/integers/set/', json=body, headers=headers, cookies=session['django-cookie'], timeout=2.50)
    xp = r.json()['integers'][0].get("X")
    dec = int.from_bytes(base64.b64decode(xp), byteorder='big')
    return dec
