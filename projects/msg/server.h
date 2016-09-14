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
#include <sstream>
#include <vector>

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
    vector<string> parse_request(string);
    void serve();
    string get_value(int, int);
    void handle(int);
    string get_request(int);
    bool send_response(int, string);
    bool needsMoreData(string&);

    int port_;
    int server_;
    int buflen_;
    char* buf_;
    string cache_;
};
