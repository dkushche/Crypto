#include <stdio.h>

struct crypto_bytearray {
    void *data;
    size_t len;
};

void print_bytearray(struct crypto_bytearray *buf);
