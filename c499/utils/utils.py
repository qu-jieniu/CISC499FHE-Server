from binascii import hexlify
from datetime import datetime
from hashlib import sha256
import json
from hashlib import sha256

with open('etc\config.json','r') as config_file:
    config = json.load(config_file)

def create_set_id():
    server_secret = sha256(config['SECRET_KEY'].rstrip().encode('utf-8')).hexdigest()
    set_id = hash(str(datetime.utcnow())+str(server_secret))
    set_utf = str(set_id).encode("utf-8")
    return hexlify(set_utf).decode('utf-8')

def strip_token(token_string):
    split = token_string.split()
    if split[0] == "Bearer":
        raise ValueError
    return split[1]

def strip_bearer(jwt_string):
    split =  jwt_string.split()
    if split[0] == "Token":
        raise ValueError
    return split[1]
