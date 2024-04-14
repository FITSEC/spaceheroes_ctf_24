all: spock scotty

spock:
	gcc -s -g -Wl,-z,relro,-z,now -o spock spock.c -lseccomp -fno-stack-protector -no-pie

scotty:
	gcc -o scotty scotty.c -no-pie

clean:
	rm spock scotty
