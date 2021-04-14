import base64
my_int = 19030341030420934240394203

print(my_int)


byted=my_int.to_bytes(32,byteorder='big')

print(byted)
print(byted.hex())

print(int(byted.hex(),16))

print(int.from_bytes(byted,byteorder='big'))

base =base64.b64encode(byted)
print(base)
unbase = base64.b64decode(base)
print(int.from_bytes(unbase,byteorder='big'))