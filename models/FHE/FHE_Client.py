import math
import os
import sys


class FHE_Client:
    def __init__(self, size):
        # self.key = crypto.generate_key()  #key for q
        self.m = int.from_bytes(os.urandom(int(size)//8), byteorder='big')
        self.p = int.from_bytes(os.urandom(int(size)//8), byteorder='big')
        while self.p <= self.m:
            self.p = int.from_bytes(os.urandom(int(size)//8), byteorder='big')


    def decrypt_int(self, xp, q, p):
        x = (xp + self.m * q) - p
        return x
