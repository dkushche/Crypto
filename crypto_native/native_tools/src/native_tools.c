
#include "native_tools.h"

void print_bytearray(struct crypto_bytearray *buf)
{
    printf("%.*s\n", (int)buf->len, (char *)buf->data);
}
