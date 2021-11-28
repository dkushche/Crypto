#include <string.h>
#include <openssl/evp.h>
#include <openssl/rsa.h>
#include <openssl/pem.h>

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

    int res;
    int temp_len;

    init(ctx, cipher, NULL, (unsigned char *)in_args->key->data,
                            (unsigned char *)in_args->iv->data);

    if (!update(ctx, out->data, &temp_len, in_args->data->data, in_args->data->len))
    {
        res = 1;
        goto err;
    }

    if (!final(ctx, out->data + temp_len, &out->len))
    {
        res = 2;
        goto err;
    }
    out->len += temp_len;

    res = 0;

err:
    EVP_CIPHER_CTX_cleanup(ctx);

    return res;
}

int rsa_generate_keys(unsigned long key_length, unsigned long exponent,
                      char *pem_key_filename, char *pub_key_filename)
{
    RSA *ctx = RSA_new();
    BIGNUM *bn = BN_new();
    int res;

    BN_set_word(bn, exponent);

    if (!RSA_generate_key_ex(ctx, key_length, bn, NULL))
    {
        res = 1;
        goto err;
    }

    FILE *pem = fopen(pem_key_filename, "w");
    if (pem == NULL)
    {
        res = 2;
        goto err;
    }

    FILE *pub = fopen(pub_key_filename, "w");
    if (pub == NULL)
    {
        res = 3;
        goto err_pub_create;
    }

    if (!PEM_write_RSAPrivateKey(pem, ctx, NULL, NULL, 0, NULL, NULL))
    {
        res = 4;
        goto err_write;
    }

    if (!PEM_write_RSAPublicKey(pub, ctx))
    {
        res = 5;
        goto err_write;
    }

    res = 0;

err_write:
    fclose(pub);

err_pub_create:
    fclose(pem);

err:
    BN_free(bn);
    RSA_free(ctx);

    return res;
}

int rsa_encrypt(struct crypto_bytearray *data,  struct crypto_bytearray *out,
                char *pub_key_filename)
{
    int res;

    FILE *pub = fopen(pub_key_filename, "r");
    if (pub == NULL)
    {
        res = 1;
        goto err;
    }

    RSA *ctx = PEM_read_RSAPublicKey(pub, NULL, NULL, NULL);
    out->len = RSA_public_encrypt(data->len, data->data, out->data, ctx, RSA_NO_PADDING);
    if (out->len < 0)
    {
        res = 2;
        goto err_encrypt;
    }

    res = 0;

err_encrypt:
    fclose(pub);
err:
    return res;
}

int rsa_decrypt(struct crypto_bytearray *data, struct crypto_bytearray *out,
                char *pem_key_filename)
{
    int res;

    FILE *pem = fopen(pem_key_filename, "r");
    if (pem == NULL)
    {
        res = 1;
        goto err;
    }

    RSA *ctx = PEM_read_RSAPrivateKey(pem, NULL, NULL, NULL);
    out->len = RSA_private_decrypt(data->len, data->data, out->data, ctx, RSA_NO_PADDING);
    if (out->len < 0)
    {
        res = 2;
        goto err_decrypt;
    }

    res = 0;

err_decrypt:
    fclose(pem);
err:
    return res;
}
