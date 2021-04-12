import uuid
import os
import requests
import json

# uuid0 = uuid.uuid4()
# password = os.urandom(8)
session = {}

uuid0 = 'jie1234'
password = 'su365792'

''' SIGNUP - GET DEVICE TOKEN AND COOKIES '''
# url = 'http://127.0.0.1:8000/api/auth/signup/'
# body = {'username':str(uuid0), 'password1':str(password), 'password2':str(password)}
# r = requests.post(url, data=body)
# print(r.json())
# session['deviceToken'] = json.loads(r.text)["token"]
# cookies = r.cookies.get_dict()
# # print(json.loads(r.text)['formError'] == {'username': ['A user with that username already exists.']})


''' LOGIN '''
url = 'http://127.0.0.1:8000/api/auth/login/'
body = {'username':str(uuid0), 'password':str(password)}
r = requests.post(url, data=body)
session['deviceToken'] = json.loads(r.text)["token"]
cookies = r.cookies.get_dict()
# print(r.cookies.get_dict())

''' GET JWT KEY PAIR '''
headers = {"Authorization":"Token " + session['deviceToken'] }
# print(headers)
r = requests.get('http://127.0.0.1:8000/api/jwt/', headers=headers, timeout=2.50)
# print(r.json())

#
''' POST A INT '''
headers = {"Authorization": "Bearer " + r.json()['access']}
body= {
	"integers":[{"index":0,"X":1,"q":1},{"index":1,"X":2,"q":2},{"index":2,"X":3,"q":3}]
	}
r = requests.post('http://127.0.0.1:8000/integers/set/', data=body, headers=headers, cookies=cookies, timeout=2.50)
print(r.text)
#
# file = open('jwt.html', 'w+')
# file.write(r.text)
# file.close()
# print(r)
