def xor_file(input_file, output_file, key):
    with open(input_file, 'rb') as f:
        input_data = f.read()

    # XOR each byte with the key
    output_data = bytearray()
    for byte in input_data:
        print(byte)
        output_data.append((byte ^ key) % 256)

    with open(output_file, 'wb') as f:
        f.write(output_data)

if __name__ == "__main__":
    # input_file = input("Enter the input file path: ")
    # output_file = input("Enter the output file path: ")
    key = 209448

    xor_file('script.txt', 'file.enc', key)
    print("XOR operation completed.")
