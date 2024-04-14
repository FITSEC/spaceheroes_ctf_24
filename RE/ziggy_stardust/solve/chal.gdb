set architecture riscv
set sysroot /usr/riscv64-linux-gnu/
file ./chal
target remote 127.0.0.1:9000

b *0x0001c58a
c

print $t4-82
c
print $t4-82
c
print $t4-82
c
print $t4-82
c
print $t4-82
c
print $t4-82
c
print $t4-82
c
print $t4-82
c
print $t4-82
c
print $t4-82
c
print $t4-82
c
print $t4-82
c
print $t4-82
c
print $t4-82
c
print $t4-82
c
print $t4-82
c
print $t4-82
c
print $t4-82
c
print $t4-82
c
print $t4-82
c
print $t4-82
c
print $t4-82
c
print $t4-82
c
print $t4-82
c
print $t4-82
c
print $t4-82
c
print $t4-82
c
print $t4-82
c
print $t4-82
c
print $t4-82
c
print $t4-82
c
print $t4-82
c
print $t4-82
c
print $t4-82
c
print $t4-82
c
print $t4-82




























#

# pre rebuild, optimizations + strip, found flag.tx go up see math be inside loop
#b *0x0001d42c

#c
#









#info functions 
#b std.start.posixCallMainAndExit
#c
#b *(0x0001cfb0+68)

# b std.os.write

# line 39
#j *0x0001d998

# line 40
# j *0x0001d9e2


##print (char*) 0x1200d
