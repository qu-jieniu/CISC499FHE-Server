import math
import base64
import os
import sys


class FHE_Client:
    def __init__(self, size):
        self.m = int.from_bytes(os.urandom(int(size)//4), byteorder=sys.byteorder)
        self.p = int.from_bytes(os.urandom(int(size)//4+1), byteorder=sys.byteorder)

    def decrypt(self, x1p, q1, x2p, q2, p, ops):
        if ops == '+':
            return (x1p + x2p) + (q1+q2)*self.m - 2*self.p
        if ops == "*":
            return ((x1p * x2p) + (x1p*q2 + x2p*q1 + q1*q2*self.m) * self.m) // (p**2)
