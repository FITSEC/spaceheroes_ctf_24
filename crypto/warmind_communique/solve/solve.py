import gostcrypto
import sys

key = bytearray(b"SKYSHOCKSKYSHOCKSKYSHOCKSKYSHOCK")
iv = bytearray(b"MIDNIGHT EXIGENT")
b_size = 128

print(f"bytes: {len(key)}, bits: {len(key) * 8}")
cipher_obj = gostcrypto.gostcipher.new('magma', key, gostcrypto.gostcipher.MODE_CBC, init_vect=iv)

with open(sys.argv[1], "wb") as message:
    with open(sys.argv[2], "rb") as enc:
        buffer = enc.read(b_size)
        while len(buffer) > 0:
            cipher_data = cipher_obj.decrypt(buffer)
            message.write(cipher_data)
            buffer = enc.read(b_size)
with open(sys.argv[1], "r") as message:
    buffer = message.read(b_size)
    mess = str(buffer)
    while len(buffer) > 0:
        buffer = message.read(b_size)
        mess += buffer
    print(mess)
