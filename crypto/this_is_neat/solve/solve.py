from Crypto.Cipher import AES
import binascii

def xor(arr1, arr2):
    result = b''
    for i in range(len(arr1)):
        result += (arr1[i] ^ arr2[i]).to_bytes()
    return result

key = b"3153153153153153"
known = b"Mortimer_McMire:"

ciphertext = binascii.unhexlify(open('message.enc', 'r').read())

cipher = AES.new(key, AES.MODE_CBC)

iv = xor(known, cipher.decrypt(ciphertext[:16]))

cipher = AES.new(key, AES.MODE_CBC, iv)

plaintext = cipher.decrypt(ciphertext)

print(plaintext)
