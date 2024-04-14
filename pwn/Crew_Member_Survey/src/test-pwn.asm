top:
    mov r3, bottom;
    push r3;
    jmp;

entry:
    push rbp;
    mov rbp, rsp;
    push rsp;
    mov r0, 00000010;
    push r0;
    sub;
    mov rsp, r0;

    push rbp;
    scanf;

    push r1;

    push rbp;
    mov r1, 00000004;
    push r1;
    sub;
    push r0;

    push rbp;
    mov r0, mem;
    push r0;

    read;

    mov r3, work;
    push r3;
    call;
    leave;
    ret;

work:
    push rbp;
    mov rbp, rsp;
    push rsp;
    mov r0, 00000050;
    push r0;
    sub;
    mov rsp, r0;

    push rbp;
    mov r2, 67616c66;
    mov mem, r2;

    push rbp;
    mov r1, 00000004;
    push r1;
    sub;
    push r0;
    mov r2, 7478742e;
    mov mem, r2;

    push rbp;
    mov r1, 00000008;
    push r1;
    sub;
    push r0;
    mov r1, 00000000;
    mov mem, r1;

    push rbp;
    mov r1, 0000004c;
    push r1;
    sub;
    push r0;
    mov r0, mem;
    push r0;

    mov r0, 67616c66;
    push r0;

    cmp;
    mov r4, leave;
    push r4
    jne;

    push rbp;
    push rbp;
    mov r0, 0000004c;
    push r0;

    readfile;
    push rbp;
    prnt;

    leave:
    leave;
    ret;

bottom:
    mov r3, entry
    push r3;
    call;
