# so... I'm sorry this might take you a few (;

there is a loop you  can see taht after mucing about in gdb for a bit (run src/run.sh)

in src/chal.gdb you can see that i  break inside the loop

find flag.txt and work backwords so you find main

in main you can see a few values inc by 1

one is `i` the other is `win` (see src for details)

# TLDR

the valid input is of len 33, see the a6 register

the itirator `i` goes up by 1 each loop, see the a2 register

the `win` value increments if the i'th char in the input string is correct, see the t4 register

# also...

i could have tried to figure out how the array of 80 bit ints gets stored with this particular optomization set, but to be honist that is a problom for future me when i find a fellow i feel like rambling to on a tuesday eavning
