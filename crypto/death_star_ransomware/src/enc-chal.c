#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <openssl/evp.h>

#define BLOCK_SIZE 16

void handleErrors(void)
{
    fprintf(stderr, "Error occurred\n");
    exit(1);
}



void generate_key(int param1, int param2, int param3, uint8_t *key) {
    // Simple transformation algorithm
    key[0] = (param1 & 0xFF);
    key[1] = (param2 & 0xFF);
    key[2] = (param3 & 0xFF);
    
    for (int i = 3; i < 16; i++) {
        key[i] = key[i-3] ^ key[i-2] ^ key[i-1];
    }
}



void ecb_encrypt(const uint8_t *plaintext, int plaintext_len, const uint8_t *key,
                 uint8_t *ciphertext, int *ciphertext_len)
{
    EVP_CIPHER_CTX *ctx;
    int len;
    int ciphertext_len_total = 0;

    if (!(ctx = EVP_CIPHER_CTX_new()))
        handleErrors();

    if (1 != EVP_EncryptInit_ex(ctx, EVP_aes_128_ecb(), NULL, key, NULL))
        handleErrors();

    if (1 != EVP_EncryptUpdate(ctx, ciphertext, &len, plaintext, plaintext_len))
        handleErrors();
    ciphertext_len_total += len;

    if (1 != EVP_EncryptFinal_ex(ctx, ciphertext + len, &len))
        handleErrors();
    ciphertext_len_total += len;

    *ciphertext_len = ciphertext_len_total;

    EVP_CIPHER_CTX_free(ctx);
}

int main(int argc, char *argv[])
{


    int param1 = 123;
    int param2 = 456;
    int param3 = 789;
    uint8_t key[BLOCK_SIZE];

    generate_key(param1, param2, param3, key);




    // Read data from stdin
    fseek(stdin, 0, SEEK_END);
    long input_size = ftell(stdin);
    fseek(stdin, 0, SEEK_SET);

    // Allocate memory to hold the input data
    uint8_t *input_data = (uint8_t *)malloc(input_size);
    if (input_data == NULL)
    {
        fprintf(stderr, "Memory allocation failed.\n");
        return 1;
    }

    // Read input data from stdin
    fread(input_data, sizeof(uint8_t), input_size, stdin);

    // Allocate memory to hold the encrypted data
    uint8_t *encrypted_data = (uint8_t *)malloc(input_size);
    int encrypted_size;

    // Encrypt the input data using ECB block cipher (AES)
    ecb_encrypt(input_data, input_size, key, encrypted_data, &encrypted_size);

    // Write encrypted data to stdout
    fwrite(encrypted_data, sizeof(uint8_t), encrypted_size, stdout);

    // Free allocated memory
    free(input_data);
    free(encrypted_data);

    return 0;
}

