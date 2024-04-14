BIN = chal
SRC = $(BIN).zig
ARCH = riscv64
OS   = linux
SPE = ReleaseSmall

default:
	zig build-exe -O $(SPE) $(SRC) -target $(ARCH)-$(OS)
	#zig build-exe -O $(SPE) $(SRC) -target $(ARCH)-$(OS) --strip
	cp $(BIN) ../docker
	cp $(BIN) ../distrib

clean:
	rm $(BIN)
	rm -rf zig-cache

