#pragma once

#include <errno.h>
#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <unistd.h>
#include <sstream>

#include <string>

#include "message.h"

using namespace std;

class Server {
public:
    Server(int port);
    ~Server();

    void run();
    
private:
    void create();
    void close_socket();
    Message parse_request(string);
    void serve();
    void get_value(int, Message);
    void handle(int);
    string get_request(int);
    bool send_response(int, string);

    int port_;
    int server_;
    int buflen_;
    char* buf_;
};
