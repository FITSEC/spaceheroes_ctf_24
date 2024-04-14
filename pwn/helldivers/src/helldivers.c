#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <unistd.h>
#include <sys/mman.h>

void menu();
void win();
void preamble() __attribute__((constructor));
int validate();
uint64_t *secure();
void loadHeader();
void deployObjective();
uint16_t supermangler = 0x1337; // CHANGE NAME

// Infrastructure measure, ignore
__attribute__((constructor)) void ignore_me() {
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);
}

void main() {
    // /* PROLOGUE
    //    Generate heap address with return pointer stored
    //    place heap address as 'canary' in rbp-8
    // */
    // uint64_t *heapptr;
    // uint64_t retptr;
    // asm("mov %0, [%%rbp+8];"           
    //     : "=r" (retptr) 
    //     ::);
    // secure(retptr);
    // asm ("mov [%%rbp-0x8], %%rax;" :::);
    // END PROLOGUE



    /* PROLOGUE
       Generate heap address with return pointer stored
       place heap address as 'canary' in rbp-8
    */
    uint64_t *heapptr;
    // asm volatile ("sub %%rsp, 0x8;":::);
    asm volatile ("mov %%rdi, [%%rbp+8];"
        "call secure;"           
        ::
        :"%rdi");
    asm volatile (
         "mov %0, %%rax;" 
         : "=r" (heapptr)
         :
         :
         );
    // END PROLOGUE

    menu();     // Only thing in here


    // /* EPILOGUE
    //    Validate stack state
    //    Provides stack's 'canary' address and return pointer
    // */
    // asm volatile (
    //     "mov %%rdi, %0;"
    //     "mov %%rsi, [%%rbp-8];"
    //     "xor %%rdx, %%rdx;"
    //     "xor %%rcx, %%rcx;"
    //     "call validate;" 
    //     :                   // output
    //     : "r" (retptr)      // input
    //     :
    //     );
    // // END EPILOGUE




    /* EPILOGUE
       Validate stack state
       Provides stack's 'canary' address and return pointer
    */
    asm volatile (
        "mov %%rdi, [%%rbp+8];"
        "mov %%rsi, [%%rbp-8];"
        "xor %%rdx, %%rdx;"
        "xor %%rcx, %%rcx;"
        "call validate;" 
        :                   
        :
        :
        );
    // END EPILOGUE
}

/*

PREAMBLE

Initializes gsbase. By default without threading gsbase will not be set by glibc and appears in gdb as being at 0x0.
Intel instruction set allows for arbitrary setting of gsbase address.

Note gs segment register holds the "gsbase". All uses of gs addresses are relative addressing. For example:

mov gs:0x14, rax

This will reference offset 0x14 from the address gsbase holds.
Once gsbase is initialized, loading into relative offsets like this will be automatic.

FS and GS define the the Thread Local Storage (TLS) address space, which is used for storing process/thread specific global data.
FS commonly stores important data including stack canaries, and used often.
GS on the other hand changes usage based on the OS. Linux, from what it seems, does not really have a common use for it.
This means we can use it for whatever we want.

FS and GS bases can be seen in gdb by using 'i r sys'

*/
void preamble() {
    // Set up gs base
    uint64_t *test = mmap(NULL, sizeof(uint64_t), PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    asm("mov %%rax, %0;"
    "WRGSBASE %%rax;"
    :
    : "r" (test)
    :
    );
}

/*

VALIDATE

Verifies the integrity of the stack protection by comparing the return addresses stored on:
1. The current function stack frame
2. The heap chunk corresponding to this stack frame
3. The GS frame index corresponding to this tack frame
If all three are the same, the calling stack frame returns normally to the saved return address.
Otherwise, sends an stack smashing error message and force exits.

*/
int validate(uint64_t* rsp, uint64_t* heap) {

    /*
    PART 1
    Traverse gsbase to find top entry and save offset.
    */

    size_t offset = 0;
    uint64_t *gsbase;   

    asm volatile (
    "RDGSBASE %%r12;" 
    "mov %0, %%r12;"
    : "=r" (gsbase)
    :
    );

    // Find newest gs entry by looking for the last non-zero position.
    while (1)  {
        // If relative address is not empty, increment and skip
        if (*(gsbase+offset+1) == 0x0){
            break;
        }
        offset+=1;
    }

    /*
    PART 2
    Use discovered top position of gs to compare.
    Note that the same is not necessary for the heap, as the address of the chunk
    is stored on the stack.
    */

    uint64_t gsCan;

    //If the gs value, heap value, and rsp value are the same, return with no error.
    if ((*(gsbase+offset) == rsp) && (*heap == rsp)) {
        // empty stored pointers before returning
        *(gsbase+offset) = 0x0;
        free(heap);
        return 0;
    }
    else {
        puts("\\-\\-\\ TREASON DETECTED /-/-/");
        exit(1);
    }
    return 1;
}

/*

Generates new heap and gs positions to store new function stack return pointer.
Takes return pointer address as arg.
Returns the address of the heap slot.

*/
uint64_t *secure(uint64_t retptr) {

    /*
    Generate space on the heap, place return pointer on heap.
    Returns this address to calling function() as it is not referencable relatively like gs register is.
    */

    uint64_t *heapcan = malloc(sizeof(uint64_t));
    *heapcan = retptr;
    
    /*
    Generate space in gs, place return pointer on heap.
    Then find empty address relative to gs register to store the return pointer.
    */

    // Check gsbase to find next empty spot to save return pointer
    size_t offset = 0;
    uint64_t *gsbase; 
    
    // Retrieve gsbase and save
    asm("RDGSBASE %0;"
        : "=r" (gsbase)
        );

    // Iterate through gs offsets until an empty spot is found
    while (1)  {
        // If relative address is not empty, increment and skip
        if (*(gsbase+offset) != 0x0){
            offset += 0x1;
        }
        else {
            // Move return pointer into rax, then store into gs offset
            asm volatile ("mov %%r10, %0;"
                "mov %%gs:[%1], %%r10;" 
                :
                : "r" (retptr), "r" (offset*8)
                :
                );
            break;
        }
    }
    return heapcan;
}



/*

TODO:
1. Initial solve script
1. Randomize menu() stack state so PIE leak position isnt predictable
2. SECCOMP against execve (I don't see how having execve would help, though)
3. Cosmetic things
    3.1. Test animation over remote
    3.2. Get more animations. Woo
4. Build container, try server


Notes:
mmap and malloc addresses are random enough, so these cant be determined before runtime

On new function start:

0. SECCOMP execve

1. Load return pointer to new gs offset 
    1.1 If gs base does not point to 0x0, increment and use that position for this function. 
2. A heap chunk is created to store the return pointer, and the return pointer is saved to the heap address.
    2.1 The heap address is stored in the 'canary' position at rbp-0x8.
3. At the end of the function, the return pointer is compared against both the heap value and the gs value. 
    3.1 The heap address taken from the canary position will be checked if it is actually located in the heap.
        This means the player cannot set the address to an arbitrary spot they know with the value they want.
    3.2 The position of gs is randomized due to mmap. Players cannot normally predict or leak this position. 
    3.3 If the return pointer, heap value, and gs value all equal, the overflow check passes.
4. The gs will be vulnerable to overwrites in the submenu function.
5. Now overflow to the win() function.

On main():
make a loop with a random max count to push data to the stack. Maybe '0xBo7' for 'Bot'? or B07B100D for BOTBLOOD?
with the theme that automaton parts got all over the terminal/pad
this will not be destroyed 

*/


/*

*/

void playAnim(char* selection) {
    if (!strcmp("orbital", selection)) {
        system("bash ./assets/orbital.sh; clear;");   // Clears screen after playing
        printf("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n");
        printf("\n");
    }
    else if (!strcmp("eaglestrike", selection)) {
        system("bash ./assets/eaglestrike.sh; clear;");   // Clears screen after playing
        printf("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n");
        printf("\n");
    }
    else if (!strcmp("eagle500", selection)) {
        system("bash ./assets/eagle500.sh; clear;" );   // Clears screen after playing
        printf("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n");
        printf("\n");
    }
    else if (!strcmp("autocannon", selection)) {
        system("bash ./assets/autocannon.sh; clear;");   // Clears screen after playing
        printf("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n");
        printf("\n");
    }
}

void loadHeader(){
    system("bash ./assets/intro.sh;");   // Clears screen after playing
    printf("\n\n\n\n\n\n\n\n\n");
    system("bash ./assets/stratagems.sh");
    printf("\n\n\n");
    printf("\n");
    printf("%60s%s", "", "➡ ➡ ⬆        Orbital Precision Strike\n");
    printf("%60s%s", "", "⬆ ➡ ⬆ ➡      Eagle Airstrike\n");
    printf("%60s%s", "", "⬆ ➡ ⬇ ⬇ ⬇    Eagle 500kg Bomb\n");
    printf("%60s%s", "", "⬇ ⬅ ⬇ ⬆ ⬆ ➡  AC-8 Autocannon\n");
    printf("%60s%s", "", "⬇ ⬆ ⬇ ⬆      Mission Objective Stratagem\n\n");

    printf("%60s%s", "", "Waiting on your call, helldiver >>> \n");
}

void menu() {

    /* PROLOGUE
       Generate heap address with return pointer stored
       place heap address as 'canary' in rbp-8
    */
    uint64_t *heapptr;
    // asm volatile ("sub %%rsp, 0x8;":::);
    asm volatile ("mov %%rdi, [%%rbp+8];"
        "call secure;"           
        ::
        :"%rdi");
    asm volatile (
         "mov %0, %%rax;" 
         : "=r" (heapptr)
         :
         :
         );
    // END PROLOGUE



    // NOTE: Maybe a function for randomly picking out quotes like "For Democracy!" etc.

    // Functional program loop
    char buf1[120] = "";
    while(1) {
        loadHeader();
        gets(buf1);                    // Technically an overflow vuln, but this one can't be used for it
        
        if (!strcmp("Quit", buf1)) {
            printf("You have been a stalwart line of freedom.\n");
            printf("Any words for the aspiring young citizens back home? >>> \n");
            gets(buf1);
            break;
        }

        printf("Deploying stratagem:\n");
        printf(buf1);          // format string vulnerability
        printf("\n");

        // change comparison strings once finalized
        if (!strcmp("➡ ➡ ⬆", buf1)) {  
            // Play animation script
            playAnim("orbital");
            continue;
        } 
        else if (!strcmp("⬆ ➡ ⬆ ➡", buf1)) {
            // Play animation script
            playAnim("eaglestrike");
            continue;
        }
        else if (!strcmp("⬆ ➡ ⬇ ⬇ ⬇", buf1)) {
            // Play animation script
             playAnim("eagle500");
            continue;
        }
        else if (!strcmp("⬇ ⬅ ⬇ ⬆ ⬆ ➡", buf1)) {
            // Play animation script
             playAnim("autocannon");
            continue;
        }
        else if (!strcmp("⬇ ⬆ ⬇ ⬆", buf1)) {
            deployObjective();
            continue;
        }
    }

    /* EPILOGUE
       Validate stack state
       Provides stack's 'canary' address and return pointer
    */
    asm volatile (
        "mov %%rdi, [%%rbp+8];"
        "mov %%rsi, [%%rbp-8];"
        "xor %%rdx, %%rdx;"
        "xor %%rcx, %%rcx;"
        "call validate;" 
        :                   
        :
        :
        );
    // END EPILOGUE
}

void deployObjective() {

    // // PROLOGUE
    // uint64_t *heapptr;
    // uint64_t retptr;
    // asm("mov %0, [%%rbp+8];"           
    //     : "=r" (retptr) 
    //     ::);
    // secure(retptr);
    // asm ("mov [%%rbp-0x8], %%rax;" :::);
    // // END PROLOGUE



    /* PROLOGUE
       Generate heap address with return pointer stored
       place heap address as 'canary' in rbp-8
    */
    uint64_t *heapptr;
    // asm volatile ("sub %%rsp, 0x8;":::);
    asm volatile ("mov %%rdi, [%%rbp+8];"
        "call secure;"           
        ::
        :"%rdi");
    asm volatile (
         "mov %0, %%rax;" 
         : "=r" (heapptr)
         :
         :
         );
    // END PROLOGUE

    // Have gs value stored in variable here.
    uint64_t *gsbase; // ********* RENAME THIS LATER -- variable storing gs frame addresses
    uint64_t securitykey = 0x0;   // Probably have to change this to a string and convert to uint16_t on the fly


    printf("Aligning super destroyer...\n");
    // Read in gsbase
    asm volatile (
    "RDGSBASE %%r12;" 
    "mov %0, %%r12;"
    : "=r" (gsbase)
    :
    :
    );
    sleep(1);

    // Average C pointer type cast experience

    printf("Calculating mission integrity...\n");
    // Mangles the gsbase pointer 
    gsbase = (uint64_t*)((uint64_t)gsbase ^ supermangler);  // XOR the gsbase pointer.
    sleep(1);

    printf("Have you discussed aqcuiring the Super Earth Expedited Munitions Fund with your Democracy Officer today?\n");
    // Intended to be used to demangle the pointer, change menu()'s saved return pointer in gs
    read(0, &securitykey, 8);       // user input
    gsbase = (uint64_t*)((uint64_t)gsbase ^ (uint16_t)((securitykey & 0xFFFF)));

    printf("Consulting Democracy Officer...\n");
    sleep(1);
    
    printf("Verify mission credentials:\n");
    // Intended to be used to overwrite the gs frame for menu()
    read(0, &securitykey, 8);
    *gsbase = securitykey;
    sleep(1);

    printf("Updating...\n");
    sleep(1);
    printf("Munitions platform updated.\n");    



    // /* EPILOGUE
    //    Validate stack state
    //    Provides stack's 'canary' address and return pointer
    // */
    // asm volatile (
    //     "mov %%rdi, %0;"
    //     "mov %%rsi, [%%rbp-8];"
    //     "xor %%rdx, %%rdx;"
    //     "xor %%rcx, %%rcx;"
    //     "call validate;" 
    //     :                   // output
    //     : "r" (retptr)      // input
    //     :
    //     );
    // // END EPILOGUE

    /* EPILOGUE
       Validate stack state
       Provides stack's 'canary' address and return pointer
    */
    asm volatile (
        "mov %%rdi, [%%rbp+8];"
        "mov %%rsi, [%%rbp-8];"
        "xor %%rdx, %%rdx;"
        "xor %%rcx, %%rcx;"
        "call validate;" 
        :                   
        :
        :
        );
    // END EPILOGUE
}

/*

WIN

The intended target of this challenge.

Players are expected to circumvent the stack protection mechanism in menu() to allow a buffer overflow and ret2win.
They must do the following:

1. Recognize the format string vuln in menu()
2. Leak PIE and determine PIE base.
3. Observe that both the value stored at the heap address and the real return pointer of menu() can be modified 
   from within menu(), but the gs frame value cannot.
4. Observe that there is an arbitrary gs frame overwrite in deployObjective()
    4.1. menu's return address is stored in the same place predictably.
         So the player doesn't need to know the gsbase, they just need to know the expected relative position.
    4.2. Demangle the pointer to get the gsbase by xoring the address again with the mangle value, then
         add 8 bytes to the resulting address to get menu's position.

         NOTE: I want to provide 2 bytes of mangling, but I don't know if that would allow unintended functionality.
               Please look into this

         Ex: (in gdb)
            mangle value = 0x1337                                                   | [this is visible in disass]
            gsbase  = 0x7ffff7fc2000 -> 0x7ffff7de06ca (__libc_start_call_main+122) | [this is not visible, generated at runtime]

            Mangled gsbase = 0x7ffff7fc2000 ^ 0x1337 = 0x7ffff7fc3337

            So we know that the gsbase is being mangled by 0x1337, and that the return address of menu() is stored in the next
            8 byte offset of gsbase, so:

            Unmangle the gsbase
                0x7ffff7fc3337 ^ (0x1337+0x8) = 0x7ffff7fc2008 -> 0x5555555555b0 (menu+371)
                
            Now menu's return address is targeted by the function for overwrite.

Then:

5. Write win() address to the heap address using %n specifier, 
6. Buffer overflow to change the return pointer to win(),
7. Go to deployObjective(), and overwrite the gs frame value with the win() address. Then return to the menu(),
   and allow menu() to exit.

*/
void superearthflag() {
    char flagbuff[25];
    fscanf(fopen("flag.txt", "r"), "%s", flagbuff);
    printf(flagbuff);
}
