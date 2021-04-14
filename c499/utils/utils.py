from binascii import hexlify
from datetime import datetime
from hashlib import sha256
import json
import base64
from django.db import models


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

def to_base64(big_int):
    return base64.b64encode(big_int.to_bytes(32,byteorder='big'))

def from_base64(base):
    return int.from_bytes(base64.b64decode(base),byteorder='big')

def b64_to_bytes(base):
    return base64.b64decode(base)

def bytes_to_b64(bytes):
    return base64.b64encode(bytes)


class Base64Field(models.TextField):

    def contribute_to_class(self, cls, name):
        if self.db_column is None:
            self.db_column = name
        self.field_name = name + '_base64'
        super(Base64Field, self).contribute_to_class(cls, self.field_name)
        setattr(cls, name, property(self.get_data, self.set_data))

    def get_data(self, obj):
        return base64.decodestring(getattr(obj, self.field_name))

    def set_data(self, obj, data):
        setattr(obj, self.field_name, base64.encodestring(data))