CFLAGS = -pie -fno-builtin -Wno-all -Wno-extra -z norelro
CHAL   = pwn-ranger
SRC    = $(CHAL).c
BIN    = $(CHAL).bin

example:
	gcc -o $(BIN) $(SRC) $(CFLAGS)

clean:
	rm -rf $(BIN)
