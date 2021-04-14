import math
import base64
import os
import sys


class FHE_Client:
    def __init__(self, size):
        # self.key = crypto.generate_key()  #key for q
        size = 50
        self.m = int.from_bytes(os.urandom(int(size)//8-1), byteorder=sys.byteorder)
        self.p = int.from_bytes(os.urandom(int(size)//8), byteorder=sys.byteorder)
        while self.p <= self.m:
            self.p = int.from_bytes(os.urandom(int(size)//8), byteorder=sys.byteorder)

    def decrypt_int(self, xp, q):
        x = (xp + self.m*q) - self.p
        return x
