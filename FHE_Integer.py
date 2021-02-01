class FHE_Integer:

    def __init__(self, x0, m0, k0, ops):
        self.x = x0
        self.m = m0
        self.k = k0
        self.encrypt(ops)

    def encrypt(self, ops):
        if ops == "+":
            self.x_prime = (self.x + self.k) % self.m
            self.q = (self.x + self.k) // self.m
        if ops == "*":
            self.x_prime = (self.x * self.k) % self.m
            self.q = (self.x * self.k) // self.m

    def getContext(self):
        return self.x_prime, self.q
