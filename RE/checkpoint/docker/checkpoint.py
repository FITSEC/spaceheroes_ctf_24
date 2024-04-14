import sys, time


RED = '\033[91m'
BLUE = '\033[94m'
RESET = '\033[0m'
BUFFER_SIZE = 8

def question1():
    print("You're cruising through Tatooine with C-3PO and R2. Jawas cross your path and peep your droids.")
    print(RED + "Jawa: Giviwi mikee juwir dlauds!" + RESET)
    print(BLUE + "You: [1]No! [2](Speed off) [3]Huh? I don't know Jawaese." + RESET)
    userResponse = input("Your response: ")
    
    bufferOverflow = ""
    if len(userResponse) > BUFFER_SIZE:
        bufferOverflow = userResponse[BUFFER_SIZE:]
    if bufferOverflow == "USE":
        question2()
    else:
        print(RED + "The Jawas pulled a slick one and stole your droids successfully." + RESET)

def question2():
    print("You continue your journey when suddenly... Tuskan Raiders appear out of nowhere!")
    print(RED + "Raider: KRRRREEEERRRRRHHHH!!! ERRRRH ERH!" + RESET)
    print(BLUE + "You: [1](Try to reason with them) [2](Speed off) [3](Open fire)" + RESET)
    userResponse = input("Your response: ")

    bufferOverflow = ""
    if len(userResponse) > BUFFER_SIZE:
        bufferOverflow = userResponse[BUFFER_SIZE:]
    if bufferOverflow == "THE":
        question3()
    else:
        print(RED + "The raiders opened fire and your droid companions did not make it." + RESET)

def question3():
    print("A bounty hunter catches up to you. He's looking to collect the bounty on your droids.")
    print(RED + "Bounty Hunter: If you want to live to see you tomorrow, you're gonna hand over your droids." + RESET)
    print(BLUE + "You: [1]Or what? [2]You got the wrong droids. [3](Give up R2 and C-3PO)" + RESET)
    userResponse = input("Your response: ")

    bufferOverflow = ""
    if len(userResponse) > BUFFER_SIZE:
        bufferOverflow = userResponse[BUFFER_SIZE:]
    if bufferOverflow == "FORCE":
        question4()
    else:
        print(RED + "The bounty hunter puts you six feet under and steals your droids." + RESET)

def question4():
    print("You finally arrive to the main trading center in Tatooine. You get stopped at a checkpoint.")
    print(RED + "Trooper: How long have you had these droids?" + RESET)
    print(BLUE + "You: [1]About three or four seasons. [2]What droids? [3]They're not for sale." + RESET)
    userResponse = input("Your response: ")

    bufferOverflow = ""
    if len(userResponse) > BUFFER_SIZE:
        bufferOverflow = userResponse[BUFFER_SIZE:]
    if bufferOverflow == "LUKE":
        printFlag()
        sys.stdout.fflush(0)
        time.sleep(5)
    else:
        print(RED + "The troopers opened fire and your droid companions did not make it." + RESET)

def printFlag():
    try:
        with open("./flag.txt", 'r') as file:
            print(BLUE + file.read() + RESET)
    except FileNotFoundError:
        print("Error: flag file not found.")

question1()
