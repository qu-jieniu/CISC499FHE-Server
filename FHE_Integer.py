class FHE_Integer:
    def __init__(self, x0, p0, m0):
        self.x = x0
        self.m = m0
        self.p = p0

    def encrypt(self):
        x_prime = (self.x + self.p) % self.m
        #print("x_p in: "+str(x_prime))
        q = (self.x - x_prime + self.p) // self.m
        #print("q in: "+str(q))
        return FHE_E_Integer(x_prime,q,self.p)      

    

class FHE_E_Integer:
    def __init__(self,x_prime0,q0,p0):
        self.x_prime = x_prime0
        self.q = q0
        self.p = p0

    def decrypt(self,m):
        x = (self.x_prime + m*self.q) - self.p
        return FHE_Integer(x,self.p,m)

    def getContext(self):
        return self.x_prime, self.q


def add_e_ints(e_int_i,e_int_j,m):
    x_i = e_int_i.x_prime 
    x_j = e_int_j.x_prime
    q_i = e_int_i.q
    q_j = e_int_j.q
    p_i = e_int_i.p
    p_j = e_int_j.p
    return FHE_E_Integer(x_i+x_j,q_i+q_j,p_i+p_j)


def mult_e_ints(e_int_i,e_int_j,m):
    x_i = e_int_i.x_prime
    print("x1_prime: " + str(x_i))
    x_j = e_int_j.x_prime
    print("x2_prime: " + str(x_j))
    q_i = e_int_i.q
    print("q1: " + str(q_i))
    q_j = e_int_j.q
    print("q2: " + str(q_j))
    p_i = e_int_i.p
    print("p1: " + str(p_i))
    p_j = e_int_j.p
    print("p2: " + str(p_j))

    print("")
    calc_x1 = x_i + q_i*m - p_i
    print(calc_x1)
    calc_x2 = x_j + q_j*m - p_j
    print(calc_x2)
    print("")

    x_new = x_i*x_j
    print("x3_prime: " + str(x_new))
    
    q_new = q_i*q_j*m+x_i*q_j+x_j*q_i
    print("q3: " + str(q_new))

    p_new = calc_x1*p_j + calc_x2*p_i + (p_i*p_j)
    print("p3: " + str(p_new))

    return FHE_E_Integer(x_new,q_new,p_new)

