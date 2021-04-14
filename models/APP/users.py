import uuid
import os
import sys
import jsonpickle

from models.FHE import *


class Session:
    def __init__(self):
        self.key_size = 0
        self.session_name = ""
        self.set = {}

    def getName(self):
        return self.session_name

    def setName(self, name):
        self.session_name = name

    def setKeySize(self, key_size):
        self.key_size = key_size

    def setServerId(self, id):
        self.server_id = id

    def freeze(self):
        return jsonpickle.encode(self)
