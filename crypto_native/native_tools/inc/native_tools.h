
#define CRYPTO_STORAGE_PATH "crypto_storage/"

struct crypto_bytearray
{
    void *data;
    size_t len;
};

void print_bytearray(struct crypto_bytearray *buf);
char *form_storage_path(char *filename);
