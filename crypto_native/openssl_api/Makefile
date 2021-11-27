all: openssl_api.so

CC ?= gcc

CFLAGS := $(shell pkg-config --cflags openssl) -ansi -std=c99 -Wall
LDFLAGS := $(shell pkg-config --libs openssl)

NATIVE_TOOLS_INCLUDES := ../native_tools/inc
LIB_NATIVE_TOOLS := ../native_tools/libnative_tools.a

CFLAGS += -I$(NATIVE_TOOLS_INCLUDES)
LDFLAGS += $(LIB_NATIVE_TOOLS)

SRC = src/openssl_api.c

OBJ = $(patsubst %.c, %.o, $(SRC))

%.o: %.c $(DEPS)
		$(CC) -c -o $@ $< $(CFLAGS)

openssl_api.so: $(OBJ)
		$(CC) -shared -o $@ $^ $(LDFLAGS)

.PHONY: clean

clean:
	rm -f $(OBJ)
