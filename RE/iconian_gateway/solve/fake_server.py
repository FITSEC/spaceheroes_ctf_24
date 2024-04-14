from socket import *

s = socket(AF_INET, SOCK_STREAM)
s.bind(('127.0.0.1', 7503))
s.listen()

while True:
    (c, addr) = s.accept()
    c.recv(1)
    c.recv(100)
    c.send(b"A"*100)
    c.close()
    s.close()
