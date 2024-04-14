set architecture riscv
set sysroot /usr/riscv64-linux-gnu/
file ./chal
target remote 127.0.0.1:9000
c
