#!/usr/bin/env python3

from pwn import *
import struct
import datetime

context.terminal = ["tmux", "splitw", "-h"]
e = ELF(args.BIN)


gs = '''
continue
'''


def start():
    if args.GDB:
        return gdb.debug(e.path, gdbscript=gs)
    else:
        return process(e.path)
p = start()
now = datetime.datetime.now()

floats = [1.2, 0.8, 2.5, 3.0, 1.5, 2.0, 0.7, 1.8, 2.2, 1.0, 0.5, 2.3]
ans = []

p.recvuntil(b'>>> ')

for x in floats:
    y = str((x * 2) + (now.minute % 12))
    p.sendline(y)

p.interactive()