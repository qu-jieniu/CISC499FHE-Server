class FHE_Integer:
    def __init__(self, x0, p0, m0):
        self.x = x0
        self.m = m0
        self.p = p0

    def encrypt(self):
        x_prime = (self.x + self.p) % self.m
        print("x_p in: "+str(x_prime))
        q = (self.x - x_prime + self.p) // self.m
        print("q in: "+str(q))
        return FHE_E_Integer(x_prime,q,self.p)      

    

class FHE_E_Integer:
    def __init__(self,x_prime0,q0,p0):
        self.x_prime = x_prime0
        self.q = q0
        self.p = p0

    def decrypt(self,m):
        x = (self.x_prime + m*self.q) % self.p
        return FHE_Integer(x,self.p,m)

    def getContext(self):
        return self.x_prime, self.q


def add_e_ints(e_int_i,e_int_j,p,m):
    x_i = e_int_i.x_prime 
    x_j = e_int_j.x_prime
    q_i = e_int_i.q
    q_j = e_int_j.q
    return FHE_E_Integer(x_i+x_j,q_i+q_j,p)


def mult_e_ints(e_int_i,e_int_j,p,m):
    x_i = e_int_i.x_prime 
    x_j = e_int_j.x_prime
    q_i = e_int_i.q
    q_j = e_int_j.q
    return FHE_E_Integer(x_i * x_j,x_i*q_j+x_j*q_i+q_i*q_j*m,p)

