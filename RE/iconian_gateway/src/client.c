#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>

#define SERVER_PORT 7503
#define SERVER_HOST "127.0.0.1"
#define BUFFER_SIZE 100

char buffer[BUFFER_SIZE] = {0};

void xor(unsigned char key, unsigned char* buf, int len) {
    for (int i = 0; i < len; i++) {
        buf[i] = buf[i] ^ key;
    }
}

void logo() {
puts("                                            B@@@@@@Www,");
puts("                                            BBBBBBBBBBBBB@@w,");
puts("                                   ,,wwmW@@@BBBBBBBBBBBBBBBBBB@W,");
puts("                       ,,,,, ,w#@BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB@w");
puts("                   w@@@@@@@@@@@@@@@@@@@@BBBBBBBBBBBBBBBBBBBBBBBBBBBBB@p");
puts("                ,@@@@@@@@@@@@@@@@@@@@@@@@@@@@BBBBBBBBBBBBBBBBBBBBBBBBBB@w");
puts("              ,@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\"\"*MMBBBBBBBBBBBBBBBBBBBB@W");
puts("            ,@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@W,  `\"%@BBBBBBBBBBBBBBBBB@p");
puts("           &@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@p    `*0BBBBBBBBBBBBBBBB@");
puts("         ,@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@p     `%BBBBBBBBBBBBBBB@");
puts("        )@@@@@@@@@@@@@@@@@@MMMMMMMMMMMK@@@@@@@@@@@@@@@@@@p      %BBBBBBBBBBBBBB@");
puts("       ]@@@@@@@@@@@MM\"?`,@BBBBBBBBBBBBBBBBBB*MK@@@@@@@@@@@@      `0BBBBBBBBBBBBBB");
puts("      ,@@@@@@@MMF      ]BBBBBBBBBBBBBBBBBBBB    `*%@@@@@@@@@p      %BBBBBBBBBBBBB@");
puts("      &@@@@MBB@Dawwppww@@@BBBBBBBBBBBBBBBBBB        `YK@@@@@@p      ]BBBBBBBBBBBBBN");
puts("      @M\" @BB$@@@@@@@@@@@@@@@@BBBBBBBBBM*\"``           `*@@@@@b      %BBBBBBBBBBBBB");
puts("     '   ]BBB$@@@@@@@@@@@@@@MBBBBBBBBF                    \"%@@@p     `BBBBBBBBBBBBBb");
puts("         &BBB$@@@@@@@@@@@@@MBBBBBBBB                        `*@@      %BBBBBBBBBBBB@");
puts("         BBBB$@@@@@@@@@@@@@BBBBBBBBF                           Y@     ]BBBBBBBBBBBBB");
puts("    @@@@@BBBBR@@@@@@@@@@@@KBBBBBBBBh                 @@@@@@@@@   L  &@@BBBB`   &BBBB");
puts("    $BBBBBBBBB@@@@@@@@@@@@@BBBBBBBB@                &BBBBBBBBM      @BBBBBB    BBBBB");
puts("    ]BBBBBBBBB%@@@@@@@@@@@`BBBBBBBBB@              #BBBBBBBBBF     ,BBBBBBM    BBBBM");
puts("     BBBBBBBBBB@@@@@@@@@@@ \"BBBBBBBBBB@w        ,#BBBBBBBBBBF      &BBBBBBF   ]BBBBF");
puts("     %BBBBBBBBBR@@@@@@@@@@  \"@BBBBBBBBBBBB@@@@@BBBBBBBBBBBB\"      4BBBBBBM    @BBBM");
puts("      @BBBBBBBBBR@@@@@@@@@b   YBBBBBBBBBBBBBBBBBBBBBBBBBBM       &BBBBBBM    &BBBB");
puts("      \"BBBBBBBBBBR@@@@@@@@@     *0BBBBBBBBBBBBBBBBBBBBM*       ,@BBBBBBM    ]BBBBF");
puts("       BBBBBBBBBBB@@@@@@@@b       \"%%BBBBBBBBBBBBMM\"        ,#BBBBBBBM    4BBBBM");
puts("        \"BBBBBBBBBBB%@@@@@@@p           ``""""``           ,@BBBBBBB@\"    @BBBBF");
puts("         \"@BBBBBBBBBBB@@@@@@@p                          ,m@BBBBBBBBF    z@BBBB\"");
puts("           %BBBBBBBBBBBR@@@@@@W.                  .,w#@BBBBBBBBBM\"    ,@BBBBM");
puts("            \"0BBBBBBBBBBBB%@@@@@@@Ww,       @@@@BBBBBBBBBBBBBBM`    ,@BBBBM\"");
puts("              \"%BBBBBBBBBBBBRK@@@@@BBBBB@@@@@BBBBBBBBBBBBBM*`     a@BBBBM*");
puts("                \"%BBBBBBBBBBBBBBM@@@@BBBBBBBBBBBBBBBMM*\"`     ,w@BBBBBM\"");
puts("                  `*%BBBBBBBBBBBBBBB%M@@@BBB\"\"\"``         ,w#@BBBBBM*");
puts("                     `*0BBBBBBBBBBBBBBBBBBBB        ,,w@@BBBBBBBM\"`");
puts("                         `*%@BBBBBBBBBBBBBBB@@@@@BBBBBBBBBBBM*`");
puts("                              `\"*MMBBBBBBBBBBBBBBBBBBMM*\"`\n");
}

void win() {
    for (int i = 0; i < 100; i++) {
        if (buffer[i] == '.') {
            printf("Hacking detected.  Commencing self-destruct.\n");
            exit(-1);
        }
    }
    
    char flag[] = "shctf{wh4t5_a_n1c3_st4rf1337_c4p7a1n_l1k3_y0u_d01ng_in_4_pl4c3_l1k3_th1s}";
    printf("%s\n", flag);
}

int main(int argc, char** argv) {

    if (argc < 3) {
        printf("Usage: %s <ip_address> <port>\n", argv[0]);
        return 1;
    }

    struct sockaddr_in server_address;
    int sock = 0, retval;
    struct sockaddr_in serv_addr;

    // Creating socket file descriptor
    if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
        printf("\n Socket creation error \n");
        return -1;
    }

    memset(&serv_addr, '0', sizeof(serv_addr));

    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(atoi(argv[2]));

    // Convert IPv4 and IPv6 addresses from text to binary form
    if(inet_pton(AF_INET, argv[1], &serv_addr.sin_addr) <= 0) {
        printf("\nInvalid address/ Address not supported \n");
        return -1;
    }

    if (connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0) {
        printf("\nConnection Failed \n");
        return -1;
    }

    // Generate and send key
    srand(time(0));
    unsigned char key = rand() % 255;
    send(sock, &key, 1, 0);

    logo();

    // Send and receive messages
    for (int i = 0; i < 3; ++i) {
        printf(">>> ");
        scanf("%100s", buffer);
        xor(key, buffer, 100);
        send(sock, buffer, 100, 0);

        // Receive response
        retval = read(sock, buffer, BUFFER_SIZE);
        if (retval < 100) {
            printf("Invalid response from server.\n");
            break;
        }
        xor(key, buffer, 100);
        buffer[100] = 0;
        printf("\nValid chars:\n%s\n\n", buffer);

        // Check win condition
        for (int j = 0; j <= 100; j++) {
            if (j == 100) {
                win();
                close(sock);
                return 0;
            }

            if (buffer[j] == '.') {
                break;
            }
        }

        // Clear buffer for the next iteration
        memset(buffer, 0, sizeof(buffer));
    }

    close(sock);
    return 0;
}
