all: ./src/message.txt ./src/encrypt.py
	python3 ./src/encrypt.py ./src/message.txt ./distrib/encrypted.enc
solve: ./solve/solve.py ./distrib/encrypted.enc
	python3 ./solve/solve.py ./solve/message.txt ./distrib/encrypted.enc
clean: ./distrib/encrypted.enc
	rm ./distrib/encrypted.enc

.phony: clean solve all
