from pwn import *
#io = remote ('127.0.0.1', 5000)
io = remote ("spaceheroes-ziggy-stardust.chals.io", 443, ssl=True, sni="spaceheroes-ziggy-stardust.chals.io")
io.recvuntil(b'>>> ')
io.sendline('wH3R3_4R3_7h3_5p1D3R5_FR0m_m4R2?')
print(io.recvall(timeout=1).decode('utf-8').strip('\n'))
