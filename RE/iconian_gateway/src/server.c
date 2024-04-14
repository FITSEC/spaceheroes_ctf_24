#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <time.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <netinet/in.h>

#define PORT 7503
#define BUFFER_SIZE 1024

void xor(unsigned char key, unsigned char* buf, int len) {
    for (int i = 0; i < len; i++) {
        buf[i] = buf[i] ^ key;
    }
}

void game(int sockfd) {
    unsigned char *buffer = malloc(BUFFER_SIZE);
    unsigned char *response = malloc(100);
    unsigned char *solution = malloc(100);
    int retval = 0;

    // Key sharing
    retval = read(sockfd, buffer, BUFFER_SIZE);
    if (retval <= 0) {
        printf("No data read from client. Killing child.\n");
        free(buffer);
        return;
    }

    unsigned char key = buffer[0];
    printf("Key received: %1p\n", key);

    // Generate random string
    srand(time(NULL));

    for (int i = 0; i < 100; i++) {
        solution[i] = (rand() % 62) + 0x41;
    }
    solution[100] = 0;

    printf("Solution generated: %s\n", solution);

    // Main loop
    for (int j = 0; j < 3; j++) {
        memset(buffer, 0, BUFFER_SIZE);
        retval = read(sockfd, buffer, BUFFER_SIZE);
        if (retval <= 0) {
            printf("Client disconnected or error reading data. Exiting child process.\n");
            break;
        }
        buffer[retval] = 0; // Null-terminate the string
        xor(key, buffer, retval);
        printf("Client guessed: %s\n", buffer);
        
        // Generate response
        for (int i = 0; i < 100; i++) {
            if (i > retval) { // guess was too short
                response[i] = '.';
                continue;
            }

            if (buffer[i] == solution[i]) {
                response[i] = solution[i];
            }
            else {
                response[i] = '.';
            }
        }

        printf("Response generated: %s\n", response);

        xor(key, response, 100);

        send(sockfd, response, 100, 0); // Send the response
    }

    printf("Game over\n");

    free(solution);
    free(response);
    free(buffer);
}

int main() {
    int server_fd, new_socket;
    struct sockaddr_in address;
    int opt = 1;
    int addrlen = sizeof(address);
    char *message = "Echo from server: ";

    // Creating socket file descriptor
    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0) {
        perror("socket failed");
        exit(EXIT_FAILURE);
    }

    // Forcefully attaching socket to the port 8080
    if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT, &opt, sizeof(opt))) {
        perror("setsockopt");
        exit(EXIT_FAILURE);
    }
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(PORT);

    // Forcefully attaching socket to the port 8080
    if (bind(server_fd, (struct sockaddr *)&address, sizeof(address)) < 0) {
        perror("bind failed");
        exit(EXIT_FAILURE);
    }
    if (listen(server_fd, 3) < 0) {
        perror("listen");
        exit(EXIT_FAILURE);
    }

    while (1) {
        if ((new_socket = accept(server_fd, (struct sockaddr *)&address, (socklen_t*)&addrlen))<0) {
            perror("accept");
            exit(EXIT_FAILURE);
        }

        // Forking a new process
        int pid = fork();
        if (pid < 0) {
            perror("fork failed");
            close(new_socket);
            continue;
        }

        // Child process
        if (pid == 0) {
            close(server_fd);

            game(new_socket);

            close(new_socket);
            exit(0); // End child process
        } else {
            // Parent process
            close(new_socket); // Parent doesn't need this
        }
    }

    return 0;
}

