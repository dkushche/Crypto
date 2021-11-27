#include <string.h>
#include <openssl/evp.h>

#include "native_tools.h"

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
    EVP_CIPHER_CTX *ctx =  EVP_CIPHER_CTX_new();
    int ret = 1;

    EVP_CIPHER *type = strcmp("CBC", in_args->mode) == 0 ? EVP_aes_128_cbc() : EVP_aes_128_cfb128();
    int enc = strcmp("encrypt", in_args->encrypt) == 0 ? 1 : 0;

    EVP_CipherInit_ex2(ctx, type, in_args->key, in_args->iv, enc, NULL);

    int temp_len;

    if (!EVP_CipherUpdate(ctx, out->data, &temp_len, in_args->data->data, in_args->data->len))
    {
        goto err;
    }

    if (!EVP_CipherFinal_ex(ctx, out->data + temp_len, &out->len))
    {
        goto err;
    }

    ret = 0;

err:
    EVP_CIPHER_free(type);
    EVP_CIPHER_CTX_free(ctx);

    return ret;
}
