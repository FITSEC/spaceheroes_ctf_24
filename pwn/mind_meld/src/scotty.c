#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <signal.h>

/*
char thought1[] = "Aye, the haggis is in the fire for sure.";
char thought2[] = "A keyboard. How quaint.";
char thought3[] = "Mad! Loony as an Arcturian dogbird!";
char thought4[] = "I'll not take that, Mr. Spock! That transporter was functioning perfectly! Transport me down right now and I'll explain to those… gentlemen…";
*/

char *thought1;
char *thought2;
char *thought3;
char *thought4;

void think_about(char* flag) {
    thought1 = malloc(150);
    thought2 = malloc(150);
    thought3 = malloc(150);
    thought4 = malloc(150);

    strncpy(thought1, flag, 150);
    strncpy(thought2, "A keyboard. How quaint.", 150);
    strncpy(thought3, "Mad! Loony as an Arcturian dogbird!", 150);
    strncpy(thought4, "I'll not take that, Mr. Spock! That transporter was functioning perfectly! Transport me down right now and I'll explain to those… gentlemen…", 150);
}

int main(int argc, char **argv) {
    think_about(argv[1]);
    
    FILE *pid_fp = fopen("pid.txt", "w");
    fprintf(pid_fp, "%d", getpid());
    fclose(pid_fp);

    while(1) {
        raise(SIGSTOP);
    }

    return 0;
}
