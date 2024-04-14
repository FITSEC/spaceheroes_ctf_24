#include <stdio.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <signal.h>
//#include <windows.h>
#include <unistd.h>

#define MEMORY_SIZE 2400

long analyze();
void win();
void fail();


// Required by assignment description
__attribute__((constructor)) void ignore_me() {
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);
}

void segfault_handler(int signum) {
    printf("ERRRRRRRRRRRRRRRRRRRRRRRRRRRR");
    exit(1);
}

int main() {
    struct sigaction sa;
    sa.sa_handler = segfault_handler;
    sa.sa_flags = 0;
    sigemptyset(&sa.sa_mask);
    if (sigaction(SIGSEGV, &sa, NULL) == -1) {
        perror("sigaction");
        return 1;
    }
    long addr = analyze();
    // const char *result = analyze();
    // char *ignore;
    // long addr = strtol(result, &ignore, 2); // The result of analyze() should be the int of win()'s address
    typedef void (*Winptr)();
    Winptr winfunc = (Winptr)addr;
    
    winfunc();

   return 0;
}

void win(){
    char flagbuff[25];
    fscanf(fopen("flag.txt", "r"), "%s", flagbuff);
    printf("%s\n", flagbuff);
}

// Runs through user input, edits tape accordingly.
// Returns pointer to tape when done.
long analyze() {
    char inputbuffer[300];  // The user's instruction input
    long tape = 0; // The 'tape' to be edited. It is 6 bytes long because the win() address is 6 bytes long.        // Initialize bits as all 0s
    printf("BEEP-BOOP-DOOP!\n");
    fgets(inputbuffer, sizeof(inputbuffer), stdin);
    int ic = 0;
    char instruction[4]; // Stores instruction from input string

    // Main loop
    while (inputbuffer[ic] != '\0') {
        memcpy(instruction, &inputbuffer[ic], sizeof(instruction));
        instruction[4] = 0x00;  //null byte

        if (!strcmp(instruction, "BEEP")) {     // Rotates all individual bytes right by 1
            asm volatile( "RCR $1, %0;" 
                        : "+r" (tape)    // NOTE: +r MEANS THE VARIABLE IS READ AND WRITE
                        );   
            // Moves cursor 1 byte right
        }

        else if (!strcmp(instruction, "BOOP")) {    // Waits 10 seconds
            sleep(10);
        }

        // Retrieves time, extracts the minute decimal.
        // Uses binary of minute to mask bits at the current position 
        else if (!strcmp(instruction, "DOOP")) {    // Retrieves time. Uses minute # as bitmask
            char substr[2];
            char *ignore;
            substr[2] = '\0';
            time_t time_sec = time(NULL);
            char* timef = ctime(&time_sec);
            strncpy(substr, timef+17, 1);
            long num = strtol(substr, &ignore, 10);

            if (num % 2 != 0) {
                long mask = 1 << 23;      // should fill the leftmost bit when OR'd
                tape |= mask;        
            }
            sleep(10);  // Waits 10 seconds. Prevent people from spamming the same command.
        }
        ic+=4;
    }


    return tape;
}

// DEBUG FUNCTION
// void printBinary(const char* str) {
//     while (*str) {
//         char currentChar = *str;
//         for (int i = 7; i >= 0; i--) {
//             putchar((currentChar & (1 << i)) ? '1' : '0');
//         }
//         putchar(' '); // Add a space between bytes
//         str++;
//     }
//     printf("\n");
// }

