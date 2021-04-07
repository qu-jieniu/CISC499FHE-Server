from FHE_Integer import *
from FHE_Client import *
client = FHE_Client()
m = client.m #modulo
p = client.p #padding
print("m: "+ str(m))
print("p: "+ str(p))

operation = '*'
x1 = FHE_Integer(1330, p,m)
x2 = FHE_Integer(394, p,m)
x1_e = x1.encrypt()
x2_e = x2.encrypt()

x1_prime, q1 = x1_e.getContext()
print("x1_prime: "+ str(x1_prime))
print("q1: "+ str(q1))
x2_prime, q2 = x2_e.getContext()
print("x2_prime: "+ str(x2_prime))
print("q2: "+ str(q2))


x12_p_plus = add_e_ints(x1_e,x2_e,p,m)

x12_plus = x12_p_plus.decrypt(m)

print("x plus: "+ str(x12_plus.x))

x12_p_mult = mult_e_ints(x1_e,x2_e,p,m)

x12_mult = x12_p_mult.decrypt(m)

print("x mult: "+ str(x12_mult.x))

x_mp_mult = mult_e_ints(x12_p_mult,x12_p_plus,p,m)

x_mp = x_mp_mult.decrypt(m)

print("x mp mult: " + str(x_mp.x))