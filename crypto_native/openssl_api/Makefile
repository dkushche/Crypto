all: openssl_api.so

CC ?= gcc

CFLAGS := $(shell pkg-config --cflags openssl) -ansi -std=c99 -Wall
LDFLAGS := $(shell pkg-config --libs openssl)

SRC = src/openssl_api.c

OBJ = $(patsubst %.c, %.o, $(SRC))

%.o: %.c $(DEPS)
		$(CC) -c -o $@ $< $(CFLAGS)

openssl_api.so: $(OBJ)
		$(CC) -shared -o $@ $^ $(LDFLAGS)

.PHONY: clean

clean:
		rm -f src/openssl_api.o
