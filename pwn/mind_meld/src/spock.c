#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <fcntl.h>
#include <unistd.h>
#include <seccomp.h>
#include <errno.h>

__attribute__((naked)) void srop_gadget() {
    asm(
            "push $15\n"
            "pop %rax\n"
            "syscall\n"
            "ret"
       );
}

pid_t scottypid() {
    int fd = open("pid.txt", O_RDONLY);
    char pid_str[6];
    read(fd, pid_str, 6);
    close(fd);

    return (pid_t)atoi(pid_str);
}

void harden_mind() {
    scmp_filter_ctx ctx = seccomp_init(SCMP_ACT_KILL);

    // seccomp_rule_add(ctx, SCMP_ACT_ERRNO(EBADF), SCMP_SYS(execve), 0);
    
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(read), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(write), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(open), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(close), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(fstat), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(rt_sigreturn), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(ptrace), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(openat), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(newfstatat), 0);
    
    seccomp_load(ctx);
    seccomp_release(ctx);

    return;
}

void logo() {
    printf("                               jM??Yp\n");
    printf("                          ,F    1w@Kwp\n");
    printf("    #*\"%%p                 @     &M   1N\n");
    printf("   j`    V               ]N     @    j@\n");
    printf("   `N     N              @H .,,]H    jM\n");
    printf("    1p    1p            ]M   \"\"@p    @h\n");
    printf("jF\"\"*@     $           .@     ,M    *@\n");
    printf("1    1p.aa#MN          #F     &      @\n");
    printf("1p    @     Tp        ,H     ,M     JN\n");
    printf("JN    $p     1        &      $F     jH\n");
    printf(" @   *1N      @      jKW  aw@K   \"MM@-\n");
    printf(" 1p    $   wM*TN     &      jH      $\n");
    printf(" !N    ]N      Tp   jN      $       @\n");
    printf("  $ ,#M\"$       1p,a@      #H      jH\n");
    printf("  ]p    `N       `\"\"     wMMKp  p ,@F\n");
    printf("   N     1p  ,                  ?*T@            JwwWww,\n");
    printf("   1p    @KM*\"                    J@          #M\"     ]b\n");
    printf("    @  #M-                        JH        ,@\"      a\"\n");
    printf("    @h                          ,  N       a@F     aF\n");
    printf("    @                       ;wM*L  @     yM\"%%p   ,&-\n");
    printf("    @        ,awWMMMMM%%****\"\"      $p  ,&F      jM\n");
    printf("    M      aM*                     `@,#F       #M\n");
    printf("    H                          Jw*\" `\"        #F\n");
    printf("    @                       JM[,w            #\"\n");
    printf("    1                      A,A\"             M\n");
    printf("     N                     ,F             ,M\n");
    printf("     1                     M             aF\n");
    printf("      V                   &            ,&'\n");
    printf("       N                 &           .#F\n");
    printf("       `@                           wF\n");
    printf("        1N                       ,A\"\n");
    printf("        ]M%%K@@@@@KW          ,w#F\n");
    printf("       ,H                `T\"T@F\n");
    printf("       #                    &\n");
    printf("       `                   *\n\n\n");
}

void meld() {
    char input[0x10];

    fflush(stdout);
    fflush(stdin);
    
    printf("Scotty's mental frequency is: %d\n\n", scottypid()); 
    
    printf("My mind to your mind...\n");
    printf("Your thoughts to my thoughts >>> ");

    fflush(stdout);

    read(0, input, 1337);

    return;
}

int main() {
    harden_mind();
    logo();
    meld();

    return 0;
}
