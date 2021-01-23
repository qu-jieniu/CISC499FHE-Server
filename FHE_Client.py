#!/bin/local/python3

from cryptography.fernet import Fernet as crypto
import math
import base64


class FHE_Client:
    def __init__(self):
        self.m = crypto.generate_key()  #128-bit key
        # print(self.m)
        # print(int.from_bytes(self.m, byteorder='big'))

    def encrypt(self, obj, dataType='int'):
        if type(obj) is int:
            pass

y=FHE_Client()
