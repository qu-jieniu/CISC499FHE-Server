import math
import base64
import os
import sys
import secrets

class FHE_Integer:

    def __init__(self, x0, size):
        self.x = x0
        # self.m = secrets.randbits(size)
        # self.p = secrets.randbits(size + 8)
        # while self.p <= self.m:
        #     self.p = secrets.randbits(size + 8)
        self.m = 10
        self.p = 20

    def encrypt(self):
        x_prime_add = (self.x + self.p) % self.m
        q_add = (self.x + self.p) // self.m
        x_prime_mul = (self.x * self.p) % self.m
        q_mul = (self.x * self.p) // self.m
        return [x_prime_add, q_add, x_prime_mul, q_mul]

    def decrypt(self, xp, q):
        return (q * self.m + xp) - self.p

    def decrypt2(self, x1p, q1, x2p, q2, p, ops):
        if ops == '+':
            return (x1p + x2p) + (q1+q2)*self.m - 2*self.p
        if ops == "*":
            return ((x1p * x2p) + (x1p*q2 + x2p*q1 + q1*q2*self.m) * self.m) // (p**2)
