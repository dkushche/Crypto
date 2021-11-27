#include <string.h>
#include <openssl/evp.h>

#include "native_tools.h"

typedef enum {
    OPENSSL_API_SUCCESS,
    OPENSSL_API_UPDATE_ERROR,
    OPENSSL_API_FINAL_ERROR
} OPENSSL_API_RESULT;

struct aes_128_args
{
    struct crypto_bytearray *data;
    struct crypto_bytearray *key;
    struct crypto_bytearray *iv;
    char *mode;
    char *encrypt;
};

int aes_128(struct aes_128_args *in_args, struct crypto_bytearray *out)
{
    EVP_CIPHER *cipher = strcmp("CBC", in_args->mode) == 0 ? EVP_aes_128_cbc() : EVP_aes_128_cfb128();
    int enc = strcmp("encrypt", in_args->encrypt) == 0 ? 1 : 0;

    EVP_CIPHER_CTX *ctx = EVP_CIPHER_CTX_new();

    int (*init)(EVP_CIPHER_CTX *ctx, const EVP_CIPHER *type,
                ENGINE *impl, const unsigned char *key, const unsigned char *iv);
    int (*update)(EVP_CIPHER_CTX *ctx, unsigned char *out,
                  int *outl, const unsigned char *in, int inl);
    int (*final)(EVP_CIPHER_CTX *ctx, unsigned char *out, int *outl);

    if (enc == 1)
    {
        init = EVP_EncryptInit_ex;
        update = EVP_EncryptUpdate;
        final = EVP_EncryptFinal_ex;
    }
    else
    {
        init = EVP_DecryptInit_ex;
        update = EVP_DecryptUpdate;
        final = EVP_DecryptFinal_ex;
    }

    OPENSSL_API_RESULT res;
    int temp_len;

    init(ctx, cipher, NULL, (unsigned char *)in_args->key->data,
                            (unsigned char *)in_args->iv->data);

    if (!update(ctx, out->data, &temp_len, in_args->data->data, in_args->data->len))
    {
        res = OPENSSL_API_UPDATE_ERROR;
        goto err;
    }

    if (!final(ctx, out->data + temp_len, &out->len))
    {
        res = OPENSSL_API_FINAL_ERROR;
        goto err;
    }
    out->len += temp_len;

    res = OPENSSL_API_SUCCESS;

err:
    EVP_CIPHER_CTX_cleanup(ctx);

    return res;
}
