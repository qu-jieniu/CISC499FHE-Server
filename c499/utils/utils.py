from binascii import hexlify
from datetime import datetime

def create_set_id():
    set_id = hash(str(datetime.utcnow())+server_secret)
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
        