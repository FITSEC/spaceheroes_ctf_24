def copy_and_overwrite_data(source_file_path, target_file_path, output_file_path, num_bytes=100):
    # Read the first 'num_bytes' from the source file
    with open(source_file_path, 'rb') as file:
        data_to_copy = file.read(num_bytes)

    # Read the entire target file into memory
    with open(target_file_path, 'rb') as file:
        target_data = file.read()

    # Overwrite the beginning of the target file data with the data from the source file
    modified_data = data_to_copy + target_data[num_bytes:]

    # Write the modified data to the output file
    with open(output_file_path, 'wb') as file:
        file.write(modified_data)

# Define the file paths
source_file_path = 'in.bmp'
target_file_path = 'enc.flag'
output_file_path = 'flag.bmp'

# Call the function to perform the operation
copy_and_overwrite_data(source_file_path, target_file_path, output_file_path)

