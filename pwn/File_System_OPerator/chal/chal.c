#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <ctype.h>
#include <time.h>
#include <signal.h>
#include <sys/mman.h>
#include <sys/stat.h>

__attribute__((constructor)) void ignore_me() {
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);
}

FILE* flag = NULL;
int money = 100;

void toLowerCase(char *str) {
    for (int i = 0; str[i]; i++) {
        str[i] = tolower(str[i]);            
    }
}

void clear() {
    system("clear");
    return;
}

void print_moons() {
    printf("Welcome to the exomoons catalogue.\n");
    printf("To route the autopilot to a moons, use the word ROUTE.\n");
    printf("To learn more abou any moon, use the work INFO.\n");
    printf("----------------------------------\n");
    printf("* The Company Building    //    Buying at 150%%.\n");
    printf("\n* Experimentation\n");
    printf("* Assurance\n");
    printf("* Vow\n");
    printf("\n* Offense (Eclipsed)\n");
    printf("* March\n");
    printf("\n* Rend (Eclipsed)\n");
    printf("* Dine\n");
    printf("* Brazil\n\n");
}

void print_options() {
    printf(">MOONS\nTo see the list of moons the autopilot can route to.\n\n");
    printf(">STORE\nTo see the company store\'s selection of useful items.\n\n");
    printf(">BESTIARY\nTO see the list of wildlife on record.\n\n");
    printf(">STORAGE\nTo access objects place into storage.\n\n");
    printf(">OTHER\nTo see the list of other commands\n\n");
}

void print_bestiary() {

    printf("BESTIARY\n\nTo access a creature file, type \"INFO\" after its name.\n");
    printf("--------------------------------------------\n\n\n");
    printf("Hoarding Liams\n");
    printf("Roaming Curtices\n");
    printf("Eyeless Josh\n");
    printf("Cody-head\n");
    printf("Forest Marcus\n");
    printf("Ghost Louie\n\n");

    printf(">ADD\n");
    printf(">INFO\n\n");
    printf(">");
    // overwrite the address of one of the file with the address of flag
    // call INFO <file> and read the content of flag.txt instead
    while (1) {
        char s[32];
        read(0, s, 32);
        // check the input for INFO or ADD

        s[strcspn(s, "\n")] = 0;
        s[strcspn(s, "\r")] = 0;

        // Split the input into tokens
        char *command = strtok(s, " "); // First token should be the command
        char *subject = strtok(NULL, " "); // Second token should be the subject

        // in case i want to overwrite a fd with the flags fd and open it
        if (strncmp(s, "add", 3) == 0) {
            FILE* fp = fopen("./new.txt", "r");
            printf("File created.\nEnter Contents:\n\n>");
            read(0, fp, 0x100);
            fwrite(s, 1, 10, fp);
            printf("File updated.\n\n>");
        }
        else if (strncmp(s, "info",4)==0) {
            clear();
            if (!strcmp(subject, "cody-head")){
                FILE *file = fopen("cody.txt", "r");
                char line[256];
                while (fgets(line, sizeof(line), file) != NULL) {
                    printf("%s", line);
                }
            }
            else if (!strcmp(subject, "eyeless")){
                FILE *file = fopen("josh.txt", "r");
                char line[256];
                while (fgets(line, sizeof(line), file) != NULL) {
                    printf("%s", line);
                }
            }
            else if (!strcmp(subject, "hoarding")){
                FILE *file = fopen("liam.txt", "r");
                char line[256];
                while (fgets(line, sizeof(line), file) != NULL) {
                    printf("%s", line);
                }
            }
            else if (!strcmp(subject, "forest")){
                FILE *file = fopen("marcus.txt", "r");
                char line[256];
                while (fgets(line, sizeof(line), file) != NULL) {
                    printf("%s", line);
                }
            }
            else if (!strcmp(subject, "ghost")){
                FILE *file = fopen("louie.txt", "r");
                char line[256];
                while (fgets(line, sizeof(line), file) != NULL) {
                    printf("%s", line);
                }
            }
            else if (!strcmp(subject, "roaming")){
                FILE *file = fopen("curtice.txt", "r");
                char line[256];
                while (fgets(line, sizeof(line), file) != NULL) {
                    printf("%s", line);
                }
            }
            else {
                printf("File not found.");
            }
            printf("\n\n>");
            //FILE* fp = fopen("./new.txt", "r");
            //read(0, fp, 0x100);
            //fwrite(s, 1, 10, fp);
        }
        else {
            check_input(s);
        }
    }
}

typedef struct {
    const char* item;
    int price;
} ItemPrice;

int getPrice(const char* itemName, ItemPrice* prices, int numberOfItems) {
    for (int i = 0; i < numberOfItems; i++) {
        if (strcmp(itemName, prices[i].item) == 0) {
            return prices[i].price;
        }
    }
    return -1;
}

void print_store() {
    printf("$%i\n\n", money);
    printf("Welcome to the Company store.\nUse words BUY and INFO on any item.\nOrder tools in bulk by typing a number.\n");
    printf("---------------------------------------\n\n\n");
    printf("* Walkie-talkie  //  Price: $12\n");
    printf("* Flashlight  //  Price: $15\n");
    printf("* Shovel  //  Price: $1 (99%% discount)\n");
    printf("* Lockpicker  //  Price: $20\n");
    printf("* Pro-flashlight  //  Price: $25\n");
    printf("* Stun grenade  //  Price: $30\n");
    printf("* Boombox  //  Price: $60\n");
    printf("* TZP-Inhalant  //  Price: $120\n");
    printf("* Zap gun  //  Price: $400\n");
    printf("* Jetpack  //  Price: $700\n");
    printf("* Extension ladder  //  Price: $60\n");
    printf("* Radar-booster  //  Price: $60\n");
    printf("* Spray paint  //  Price: $50\n");
    printf("* Flag  //  price: $100\n\n");
    printf(">");

    ItemPrice prices[] = {
        {"walkie-talkie", 12},
        {"flashlight", 15},
        {"shovel", 1},
        {"lockpicker", 20},
        {"pro-flashlight", 25},
        {"stun grenade", 30},
        {"boombox", 60},
        {"tzp-inhalant", 120},
        {"zap gun", 400},
        {"jetpack", 700},
        {"extension ladder", 60},
        {"sadar-booster", 60},
        {"spray paint", 50},
        {"Flag", 100}
    };

    int numberOfItems = sizeof(prices) / sizeof(prices[0]);

    while (1) {
        char s[32];
        gets(s);

        if (!strcmp(s, "flag")) {
            int fd = fileno(flag);
            struct stat statbuf;
            fstat(fd, &statbuf);
            char *data = mmap(NULL, statbuf.st_size, PROT_READ, MAP_PRIVATE, fd, 0);
            if (money >= 100) {
                money = money - 100;
                printf("Thank you for your purchase");
                sleep(2);
                check_input("store");
            }
            else {
                printf("You don't have enough money to buy %p\n", (void*)data);
            }
        }
        else {
            int price = getPrice(s, prices, numberOfItems);
            if (price != -1 && money >= price) {
                money = money - price;
                printf("Thank you for your purchase\n new balance = %d", money);
                sleep(2);
                check_input("store");
            }
            else if (price > money) {
                
                printf("Not enough money \n");
                sleep(2);
                printf("\n>");
                continue;
            }
            else {
                check_input(s);
            }
        }
    }

    return;
}

void print_storage() {
    printf("Functionalities removed for testing\n\n");
    printf("While moving furniture with [B], you can press [x]\nto send it to storage. You can call it back from\nstorage here\n\n");
    printf("These are the items in storage:\n\n");
    printf("File Cabinet\n");
    printf("Bunkbeds\n\n");
}

void print_other() {
    printf("Functionalities removed for testing\n\n");
    printf("Other commands:\n\n");
    printf(">VIEW MONITOR\nCurrently unavailable.\n\n");
    printf(">SWITCH [name]\nCurrently unavailable.\n\n");
    printf(">PING\nTo make a radar booster play a noise.\n\n");
    printf(">TRANSMIT [message]\nTo transmit a message with the signal translator.\n\n");
    printf(">SCAN\nTo scan for the number of items lift on the current moon.\n\n");
}

void check_input(char* s) {
    //printf("input: %s\n", s);    
    if (!strcmp(s, "moons")) {
        clear();
        print_moons();
    }
    else if (!strcmp(s, "store")) { 
        clear();
        print_store();
    }
    else if (!strcmp(s, "bestiary")) { 
        clear();
        print_bestiary();
    }
    else if (!strcmp(s, "storage")) { 
        clear();
        print_storage();
    }
    else if (!strcmp(s, "other")) { 
        clear();
        print_other();
    }
    else if (!strcmp(s, "help")) { 
        clear();
        print_options();
    }
    else {
        clear();
        printf("[There was no action supplied with the word.]\n\n");
    }
}

int main() {
    clear();
    flag = fopen("./flag.txt", "r");
    printf("\033[;32mWelcome to the FORTUNE-9 OS\n           Courtesy of the Company: flag   = %p\n",&flag);
    sleep(1);
    printf("Happy %s", "Tuesday\n");
    printf("Type \"Help\" for a list of commands.\n\n");
    while (1) {
        char s[8];
        gets(s);
        check_input(&s);
    }
    return 0;
}
