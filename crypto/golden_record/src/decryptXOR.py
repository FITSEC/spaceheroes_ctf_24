def xor_file(input_file, output_file, key):
    with open(input_file, 'rb') as f:
        input_data = f.read()

    # XOR each byte with the key
    output_data = bytearray()
    for byte in input_data:
        decrypted_byte = (byte ^ key) % 256
        output_data.append(decrypted_byte)

    with open(output_file, 'wb') as f:
        f.write(output_data)

if __name__ == "__main__":
    key = 209448

    xor_file('file.enc', 'reversedXOR', key)
    print("Decryption completed.")
