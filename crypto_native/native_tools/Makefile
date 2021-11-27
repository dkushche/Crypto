all: libnative_tools.a

CC ?= gcc
AR ?= ar

CFLAGS := -ansi -std=c99 -Wall
LDFLAGS :=

CFLAGS += -Iinc/

SRC = src/native_tools.c

OBJ = $(patsubst %.c, %.o, $(SRC))

%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

libnative_tools.a: $(OBJ)
	$(AR) rcs $@ $^ $(LDFLAGS)

.PHONY: clean

clean:
	rm -f $(OBJ)
