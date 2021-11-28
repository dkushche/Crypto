#include <string.h>
#include <stdlib.h>
#include <stdio.h>

#include "native_tools.h"

void print_bytearray(struct crypto_bytearray *buf)
{
    printf("%.*s\n", (int)buf->len, (char *)buf->data);
}

char *form_storage_path(char *filename)
{
    char *path = (char *)malloc(strlen(filename) + sizeof(CRYPTO_STORAGE_PATH));

    strcpy(path, CRYPTO_STORAGE_PATH);
    strcat(path, filename);

    return path;
}
