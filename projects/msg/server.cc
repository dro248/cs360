#include "server.h"

Server::Server(int port) {
    // setup variables
    port_ = port;
    buflen_ = 10000;
    buf_ = new char[buflen_+1];
    cache_ = "";
}

Server::~Server() {
    delete buf_;
}

void
Server::run() {
    // create and run the server
    create();
    serve();
}

void
Server::create() {
    struct sockaddr_in server_addr;

    // setup socket address structure
    memset(&server_addr,0,sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(port_);
    server_addr.sin_addr.s_addr = INADDR_ANY;

    // create socket
    server_ = socket(PF_INET,SOCK_STREAM,0);
    if (!server_) {
        perror("socket");
        exit(-1);
    }

    // set socket to immediately reuse port when the application closes
    int reuse = 1;
    if (setsockopt(server_, SOL_SOCKET, SO_REUSEADDR, &reuse, sizeof(reuse)) < 0) {
        perror("setsockopt");
        exit(-1);
    }

    // call bind to associate the socket with our local address and
    // port
    if (bind(server_,(const struct sockaddr *)&server_addr,sizeof(server_addr)) < 0) {
        perror("bind");
        exit(-1);
    }

    // convert the socket to listen for incoming connections
    if (listen(server_,SOMAXCONN) < 0) {
        perror("listen");
        exit(-1);
    }
}

void
Server::close_socket() {
    close(server_);
}

void
Server::serve() {
    // setup client
    int client;
    struct sockaddr_in client_addr;
    socklen_t clientlen = sizeof(client_addr);

      // accept clients
    while ((client = accept(server_,(struct sockaddr *)&client_addr,&clientlen)) > 0) {
        while (1) {
            handle(client);
        }
    }
    close_socket();
}

vector<string> Server::parse_request(string request) {
    stringstream ss;
    ss << request;
    string field;
    vector<string> fields;
    while (ss >> field) {
        fields.push_back(field);
    }
    return fields;
}

string Server::get_value(int client,int length) {
    string request = cache_;
    cache_ = "";
    // read until we get a newline
    while (request.length() < length) {
        int nread = recv(client,buf_,buflen_,0);
        if (nread < 0) {
            if (errno == EINTR)
                continue;
            else {
                // need to retun error to client
                return request;
            }
        } else if (nread == 0) {
            //TODO: return error to client
            return request;
        }
        // be sure to use append in case we have binary data
        request.append(buf_,nread);
    }
    //clear the cache after the request has been saved into string request
    cache_ = "";
    return request;
}

bool handle_message(int client, Message msg) {
    return false;
}

bool Server::needsMoreData(string &cmd) {
    return cmd=="put";
}

void
Server::handle(int client) {
    while (1) {
        string request = get_request(client);

        if (request.empty())
            break;

        vector<string> req_fields = parse_request(request);
        Message msg = Message();

        if (needsMoreData(req_fields[0])) {
            string message = get_value(client,stoi(req_fields[3]));
            msg.setValue(message);            
        }
        msg.setCommand(req_fields[0]);

        bool success = handle_message(client,msg);

        if (not success)
            break;
    }
    close(client);
}

string
Server::get_request(int client) {
    string request = "";
    // read until we get a newline
    while (request.find("\n") == string::npos) {
        int nread = recv(client,buf_,1024,0);
        if (nread < 0) {
            if (errno == EINTR)
                // the socket call was interrupted -- try again
                continue;
            else
                // an error occurred, so break out
                return "";
        } else if (nread == 0) {
            // the socket is closed
            return "";
        }
        // be sure to use append in case we have binary data
        request.append(buf_,nread);
    }
    cache_ = "";
    //there should always be a newline
    cache_ = request.substr(request.find("\n"));
    request = request.substr(0, request.find("\n"));
    return request;
}

bool
Server::send_response(int client, string response) {
    // prepare to send response
    const char* ptr = response.c_str();
    int nleft = response.length();
    int nwritten;
    // loop to be sure it is all sent
    while (nleft) {
        if ((nwritten = send(client, ptr, nleft, 0)) < 0) {
            if (errno == EINTR) {
                // the socket call was interrupted -- try again
                continue;
            } else {
                // an error occurred, so break out
                perror("write");
                return false;
            }
        } else if (nwritten == 0) {
            // the socket is closed
            return false;
        }
        nleft -= nwritten;
        ptr += nwritten;
    }
    return true;
}
