import uuid
import os
import sys
import jsonpickle


class Session:
    def __init__(self):
        self.secret_key = int.from_bytes(os.urandom(128), byteorder=sys.byteorder)
        self.session_name = ""
    def getName(self):
        return self.session_name
    def setName(self, name):
        self.session_name = name
    def setKey(self, key_size):
        self.secret_key = int.from_bytes(os.urandom(int(key_size)//4), byteorder=sys.byteorder)
    def toJson(self):
        return jsonpickle.encode(self)
    def toDict(self):
        return jsonpickle.decode(self)
