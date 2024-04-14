CFLAGS = -Wl,-z,relro,-z,now -Wall -Wextra
CHAL   = Borson300VM
SRC    = $(CHAL).c
BIN    = $(CHAL).bin

all: ./src/$(SRC)
	cp ./src/$(SRC) ../../pwn/Crew_Member_Survey/src/
	gcc -o ./distrib/$(BIN) ./src/$(SRC) $(CFLAGS)
	gcc -o ./solve/$(BIN) ./src/$(SRC) $(CFLAGS)
	gcc -o ./docker/$(BIN) ./src/$(SRC) $(CFLAGS)

clean: ./distrib/$(BIN) ./solve/$(BIN)
	rm ./distrib/$(BIN)
	rm ./solve/$(BIN)
	rm ./docker/$(BIN)

build:
	docker buildx build -t lethal_virtualization ./docker/
