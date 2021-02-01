from FHE_Integer import *
from FHE_Client import *
from FHE_Server import *


client = FHE_Client()
m = client.m #modulo
p = client.p #padding


operation = '*'
x1 = FHE_Integer(1330, m, p, operation)
x2 = FHE_Integer(394, m, p, operation)
x1_prime, q1 = x1.getContext()
x2_prime, q2 = x2.getContext()

server = FHE_Server()
x12_p_plus = server.calc(x1_prime, x2_prime, operation)

x12_plus = client.decrypt(x1_prime, q1, x2_prime, q2, p, operation)

print(x12_plus)
