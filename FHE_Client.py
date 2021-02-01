#!/bin/local/python3

from cryptography.fernet import Fernet as crypto
import math
import base64
import os


class FHE_Client:
    def __init__(self):
        self.key = crypto.generate_key()  #key for q
        self.m = int.from_bytes(os.urandom(4), byteorder="big") #16-byte modolo

        self.p = int.from_bytes(os.urandom(4), byteorder="big")
        while self.p <= self.m:
            self.p = int.from_bytes(os.urandom(4), byteorder="big")

    def decrypt(self, x1p, q1, x2p, q2, p, ops):
        if ops == '+':
            return (x1p + x2p) + (q1+q2)*self.m - 2*self.p
        if ops == "*":
            return ((x1p * x2p) + (x1p*q2 + x2p*q1 + q1*q2*self.m) * self.m) // (p**2)
