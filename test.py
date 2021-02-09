from FHE_Integer import *
from FHE_Client import *
from FHE_Server import *
from FHE_Polynomial import *


client = FHE_Client()
m = client.m #modulo
p = client.p #padding
print("m: "+ m)
print("p: "+ p)

operation = '*'
x1 = FHE_Integer(1330, m, p, operation)
x2 = FHE_Integer(394, m, p, operation)
x1_prime, q1 = x1.getContext()
print("x1_prime: "+ x1_prime)
print("q1: "+q1)
x2_prime, q2 = x2.getContext()
print("q2: "+ q2)
server = FHE_Server()
x12_p_plus = server.calc(x1_prime, x2_prime, operation)

x12_plus = client.decrypt(x1_prime, q1, x2_prime, q2, p, operation)

print(x12_plus)
