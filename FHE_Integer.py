class FHE_Integer:
    def __init__(self, x0, p0, m0):
        self.x = x0
        self.m = m0
        self.p = p0

    def encrypt(self):
        x_prime = (self.x + self.p) % self.m
        q = (self.x - x_prime + self.p) // self.m
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
    x_prime_i = e_int_i.x_prime
    x_prime_j = e_int_j.x_prime
    
    q_i = e_int_i.q
    q_j = e_int_j.q

    p_i = e_int_i.p
    p_j = e_int_j.p

    x_i = x_prime_i + q_i*m - p_i
    x_j = x_prime_j + q_j*m - p_j
 

    x_k = x_i*x_j
    
    q_k = q_i*q_j*m+x_i*q_j+x_j*q_i

    p_k = calc_x1*p_j + calc_x2*p_i + (p_i*p_j)

    return FHE_E_Integer(x_k,q_k,p_k)

def mult_e_ints_m(e_int_i,e_int_j,m_i,m_j):
    x_i = e_int_i.x_prime
    x_j = e_int_j.x_prime
    
    q_i = e_int_i.q
    q_j = e_int_j.q
    
    p_i = e_int_i.p
    p_j = e_int_j.p

    calc_x1 = x_i + q_i*m_i - p_i
    calc_x2 = x_j + q_j*m_j - p_j

    x_k = x_i*x_j
    
    q_k = 1 + x_i/(q_i*m_i) + x_j/(q_j*m_j) 

    p_k = calc_x1*p_j + calc_x2*p_i + (p_i*p_j)

    m_k = q_i*m_i*q_j*m_j
    return FHE_E_Integer(x_new,q_new,p_new).decrypt(m_k)