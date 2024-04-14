#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <time.h>

#define True 1

void print_flag() {
    FILE* f = fopen("flag.txt", "r");
    char flag[50];
    fgets(flag, 50, f);
    printf("<<< %s\n", flag);
}

int atm(char c) {
    if(c == 'w') {
        printf("How much would you like to withdrawal? (Whole amts only)\nAmount: \n");
        int amt;
        scanf("%d", &amt);

        srand((unsigned int)time(NULL));
        int num = rand();
        
        if(amt == num) {
            print_flag();
            return 1;
        }
        printf("Completing facial recognition...\n");
        sleep(2);
        printf("Wait a minute, this isn't you! Locking in time loop...\n");
        sleep(2);
        printf("Going back in time... beep boop beep beep boop\n");
        sleep(2);
    }
    else if(c == 'b') {
        printf("Balance: 100,000,000,000 AD (Alien Dollars)\n");
    }
    return 0;
}

int main() {
    printf("Welcome to the ATM (Alien Time Machine)! Please select an option from the list below:\n");
    while(True) {
        char input;
        printf("(b)alance\n(w)ithdrawal\nOption: \n");
        scanf("%c", &input);
        getchar(); // consume newline character
        if(atm(input) == 1) {
            break;
        };
    }
    print_flag();
    return 0;
}
