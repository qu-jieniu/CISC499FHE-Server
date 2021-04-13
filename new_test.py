from FHE_Integer import *
from FHE_Client import *

client = FHE_Client()
m = client.m #modulo
p = client.p #padding
print("m: "+ str(m))
print("p: "+ str(p))

int1 = -31423525121
int2 = 51231431535

'''
x1 = FHE_Integer(-15125124131, p,m)
x2 = FHE_Integer(124125532325, p,m)
x1_e = x1.encrypt()
x2_e = x2.encrypt()


x12_p_plus = add_e_ints(x1_e,x2_e,m)

x12_plus = x12_p_plus.decrypt(m)

print("plus should be: " + str(-15125124131+124125532325))
print("x plus: "+ str(x12_plus.x))
'''

'''
x1 = FHE_Integer(int1, p,m)
x2 = FHE_Integer(int2, p,m)
x1_e = x1.encrypt()
x2_e = x2.encrypt()

x12_p_mult = mult_e_ints(x1_e,x2_e,m)

x12_mult = x12_p_mult.decrypt(m)

print(int1*int2)
print("x mult: "+ str(x12_mult.x))
'''

x1 = FHE_Integer(int1, p,m+7)
x2 = FHE_Integer(int2, p,m)
x1_e = x1.encrypt()
x2_e = x2.encrypt()

x12_p_mult = mult_e_ints2(x1_e,x2_e,m+7,m)



print(int1*int2)
print("x mult: "+ str(x12_p_mult.x))




'''
x1 = FHE_Integer(int1, p,m)
x2 = FHE_Integer(int2, p,m)
x1_e = x1.encrypt()
x2_e = x2.encrypt() 

x1_prime, q1 = x1_e.getContext()
print("x1_prime: "+ str(x1_prime))
print("q1: "+ str(q1))
x2_prime, q2 = x2_e.getContext()
print("x2_prime: "+ str(x2_prime))
print("q2: "+ str(q2))


x12_p_plus = add_e_ints(x1_e,x2_e,m)

x12_plus = x12_p_plus.decrypt(m)

print("plus should be: " + str(int1+int2))
print("x plus: "+ str(x12_plus.x))

x12_p_mult = mult_e_ints(x1_e,x2_e,m)

x12_mult = x12_p_mult.decrypt(m)

print(int1*int2)
print("x mult: "+ str(x12_mult.x))

x_mp_mult = mult_e_ints(x12_p_mult,x12_p_plus,m)

x_mp = x_mp_mult.decrypt(m)

print("mp mult should be: " + str((int1*int2)*(int1+int2)))
print("x mp mult: " + str(x_mp.x))
'''