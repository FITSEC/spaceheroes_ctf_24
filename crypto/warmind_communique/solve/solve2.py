import gostcrypto
key = bytearray(b"SKYSHOCKSKYSHOCKSKYSHOCKSKYSHOCK")
iv = bytearray(b"V150NLK747CLS000")

b_size = 128
cipher_obj = gostcrypto.gostcipher.new('magma', key, gostcrypto.gostcipher.MODE_CBC, init_vect=iv)
with open("../distrib/encrypted.enc", "rb") as f:
    buffer = f.read(b_size)
    while len(buffer) > 0:
        cipher_data = cipher_obj.decrypt(buffer)
        print(cipher_data)
        buffer = f.read(b_size)
    
    