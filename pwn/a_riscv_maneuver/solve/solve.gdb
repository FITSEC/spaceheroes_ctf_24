set architecture riscv
set sysroot /usr/riscv64-linux-gnu/
file ./chal
target remote 127.0.0.1:9000

b main
b *0x000000000001083e
disassemble main
c
c
# disassembles shellcode
#x/20i 0x4000800b20

#disassemble gadget0
#disassemble gadget1



#print (char*) 0x1200d
