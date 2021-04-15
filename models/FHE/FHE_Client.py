import math
import os
import sys


class FHE_Client:
    def __init__(self, size):
        # self.key = crypto.generate_key()  #key for q
        # self.m = int.from_bytes(os.urandom(int(size)//8), byteorder=sys.byteorder)
        # self.p = int.from_bytes(os.urandom(int(size)//8), byteorder=sys.byteorder)
        # while self.p <= self.m:
        #     self.p = int.from_bytes(os.urandom(int(size)//8), byteorder=sys.byteorder)
        self.m = 10
        self.p = 11

    def decrypt_int(self, xp, q, p):
        x = (xp + self.m * q) - p
        return x
