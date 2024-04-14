CFLAGS = -Wl,-z,relro,-z,now -Wall -Wextra
CHAL   = Borson300VM
SRC    = $(CHAL).c
BIN    = $(CHAL).bin
BC     = pwnable

all: ./src/$(SRC)
	python3 ./src/assembler.py ./src/test-pwn.asm ./distrib/pwnable ./docker/pwnable ./solve/pwnable
	gcc -o ./distrib/$(BIN) ./src/$(SRC) $(CFLAGS)
	gcc -o ./solve/$(BIN) ./src/$(SRC) $(CFLAGS)
	gcc -o ./docker/$(BIN) ./src/$(SRC) $(CFLAGS)

clean: ./distrib/$(BIN) ./solve/$(BIN)
	rm ./distrib/$(BC)
	rm ./solve/$(BC)
	rm ./docker/$(BC)
	rm ./distrib/$(BIN)
	rm ./solve/$(BIN)
	rm ./docker/$(BIN)

build:
	docker buildx build -t crew_member_survey ./docker/
