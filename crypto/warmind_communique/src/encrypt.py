import gostcrypto
import sys

key = bytearray(b"SKYSHOCKSKYSHOCKSKYSHOCKSKYSHOCK")
iv = bytearray(b"MIDNIGHT EXIGENT")
b_size = 64
print(key)
print(iv)
print(f"bytes: {len(key)}, bits: {len(key) * 8}")
cipher_obj = gostcrypto.gostcipher.new('magma', key, gostcrypto.gostcipher.MODE_CBC, init_vect=iv)

with open(sys.argv[1], "rb") as message:
    with open(sys.argv[2], "wb") as enc:
        buffer = message.read(b_size)
        while len(buffer) > 0:
            cipher_data = cipher_obj.encrypt(buffer)
            enc.write(cipher_data)
            buffer = message.read(b_size)