import base64
import json
import math

int1 = 17
int2 = 15

needed1 = math.ceil(int1.bit_length()/8)
base1 = base64.b64encode(int1.to_bytes(length=needed1,byteorder='big'))
print("base64 encoding int1: "+str(base1))

needed2 = math.ceil(int2.bit_length()/8)
base2 = base64.b64encode(int2.to_bytes(length=needed2,byteorder='big'))
print("base64 encoding int2: "+str(base2))  

encoded = b'8A=='

# 2d32303131323935323737323736303437383634
# 2d33343335333533383634323937393438333238

result =  base64.b64decode("8A==")
print(int.from_bytes(result,byteorder='big'))

# sum 34393937383637373938303531343437373231

t_dict = {'X':encoded}

tson = json.dumps(t_dict)
print(tson)