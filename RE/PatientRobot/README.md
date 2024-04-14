# PatientRobot

## Prompt

This old floor cleaning bot ate my flag! Its one of those old models with an obscure language chip installed, which is only made worse by its sluggish response times. I'm losing my patience!

## Solution

Main's only function is to call analyze and then call the result of analyze.
Debuggers may represent this as analyze()().

The binary has a win() function as a target.

The input of analyze has three cases:

1. BEEP
   Bitwise rotate an integer right once
   ```
   004013dd          int32_t rax_5 = strcmp(&var_16c, "BEEP")
   004013e4          if ((rax_5 & rax_5) == 0)
   004013ed              var_10 = rrc.q(var_10, 1, false)
   ```
2. BOOP
   Sleep for 10 seconds
   ```
   004013e4          else if (strcmp(&var_16c, "BOOP") == 0)
   00401418              sleep(seconds: 0xa)
   ```
3. DOOP
   First gets the system time, then copies the 17th character. This happens to be the 10's seconds place.
   It performs a bitwise AND with 1. If the result is 1, the integer buffer is OR'd with 0x800000.
   This effectively means that if the current 10s place of the seconds is odd, such as 10, 30, 50, etc, then this command inserts a bit into the integer.
   Lastly, this command sleeps for 10 seconds.
   ```
   00401411          else if (strcmp(&var_16c, "DOOP") == 0)
   00401443              var_16c.b = 0
   00401454              time_t t = time(nullptr)
   00401488              void nptr
   00401488              strncpy(&nptr, &ctime(t: &t)[0x11], 1)
   004014b9              void endptr
   004014b9              if (zx.q(strtol(nptr: &nptr, endptr: &endptr, base: 0xa) & 1) != 0)
   004014c7                  var_10 = var_10 | 0x800000
   004014d0              sleep(seconds: 0xa)
   ```

The integer buffer that is modified by these commands is also returned to main where it is called as a function.
Since we are modifying a function pointer and have win() in the binary, the natural goal would be to construct the address of win().

So we must find some combination of these four-character commands to manipulate the integer to equal the address of win().

This is a type of puzzle, but consider this:
1. Since inserting a bit only works on odd 10s seconds but then sleeps for 10, every call of DOOP must be followed by BOOP to return to an odd time
2. Rotating does not sleep, so we can rotate as much as we want in between inserting bits.

So lets get the address of win:

```
addr = bin(e.sym['win'])[::-1].strip('b0') # Win addr
```

Note that we must reverse the order of the bits to preserve endianness.

Now each time we see a 1 in the address, we must insert a bit and rotate over once to make room for the next bit.
This also means we must sleep after each bit insert so that the next time is still an odd time.

Each time we see a 0, we can just rotate immediately and try the next bit. 

```
response = ""
for bit in addr:
    if bit == "1":
        response += "DOOPBOOPBEEP"
    elif bit == "0":
        response += "BEEP"
```

And that should construct the address of win. The binary will have to verify the solution after 2 minutes.
Make sure to have your script wait enough time to cover that:

```
print(p.recvline(timeout=200))
```

Remember that since the check for inserting a bit is at an odd numbered digit, the script must be started at times such as
11:17:10
11:17:30
11:17:50
11:18:10
...
where the 10s second is odd.


## Script

```
from pwn import *

e = context.binary = ELF(args.BIN)

# Must be run at a time where the 10's seconds position is odd:
# 06:07:10 , 06:07:30 , 06:07:50 etc.
# https://time.is/

p = process(e.path)
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
```
