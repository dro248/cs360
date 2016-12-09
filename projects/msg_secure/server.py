from Crypto.PublicKey import RSA
from Crypto import Random
import optparse
import socket
import sys
import select
import errno
import traceback

import logging
import argparse

class Server:
    def __init__(self,port):
        self.host = ""
        self.port = port
        self.clients = {}
        self.caches = {}
        self.messages = {}
        self.keys = {}
        self.size = 10024
        self.open_socket()
        self.run()

    def open_socket(self):
        """ Setup the socket for incoming clients """
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
            self.server.bind((self.host,self.port))
            self.server.listen(5)
            self.server.setblocking(0)
        except socket.error, (value,message):
            if self.server:
                self.server.close()
            print "Could not open socket: " + message
            sys.exit(1)

    def run(self):
        """ Use poll() to handle each incoming client."""
        self.poller = select.epoll()
        self.pollmask = select.EPOLLIN | select.EPOLLHUP | select.EPOLLERR
        self.poller.register(self.server,self.pollmask)
        while True:
            # poll sockets
            try:
                fds = self.poller.poll(timeout=1)
            except:
                return
            for (fd,event) in fds:
                # handle errors
                if event & (select.POLLHUP | select.POLLERR):
                    self.handle_error(fd)
                    continue
                # handle the server socket
                if fd == self.server.fileno():
                    self.handle_server()
                    continue
                # handle client socket
                result = self.handle_client(fd)

    def handle_server(self):
        # accept as many clients as possible
        while True:
            try:
                (client,address) = self.server.accept()
            except socket.error, (value,message):
                # if socket blocks because no clients are available,
                # then return
                if value == errno.EAGAIN or errno.EWOULDBLOCK:
                    return
                print traceback.format_exc()
                sys.exit()
            # set client socket to be non blocking
            client.setblocking(0)
            self.clients[client.fileno()] = client
            self.caches[client.fileno()] = ""
            self.poller.register(client.fileno(),self.pollmask)

    def handle_error(self,fd):
        self.poller.unregister(fd)
        if fd == self.server.fileno():
            # recreate server socket
            self.server.close()
            self.open_socket()
            self.poller.register(self.server,self.pollmask)
        else:
            # close the socket
            self.clients[fd].close()
            del self.clients[fd]

    def handle_client(self,fd):
        try:
            data = self.clients[fd].recv(self.size)
        except socket.error, (value,message):
            # if no data is available, move on to another client
            if value == errno.EAGAIN or errno.EWOULDBLOCK:
                return
        if not data:
            return
        self.caches[fd] += data
        message = self.read_message(fd)
        if not message:
            return
        self.handle_message(message,fd)

    def read_message(self,fd):
        index = self.caches[fd].find("\n")
        if index == "-1" or index == -1:
            return None
        message = self.caches[fd][0:index+1]
        self.caches[fd] = self.caches[fd][index+1:]
        return message

    def handle_message(self,message,fd):
        response = self.parse_message(message,fd)
        self.send_response(response,fd)

    def parse_message(self,message,fd):
        fields = message.split()
        if not fields:
            return('error invalid message\n')
        if fields[0] == 'reset':
            self.messages = {}
            return "OK\n"
        if fields[0] == 'put':
            try:
                name = fields[1]
                subject = fields[2]
                length = int(fields[3])
            except:
                return('error invalid message\n')
            data = self.read_put(length,fd)
            if data == None:
                return 'error could not read entire message\n'
            self.store_message(name,subject,data)
            return "OK\n"
        if fields[0] == 'list':
            try:
                name = fields[1]
            except:
                return('error invalid message\n')
            subjects,length = self.get_subjects(name)
            response = "list %d\n" % length
            response += subjects
            return response
        if fields[0] == 'get':
            try:
                name = fields[1]
                index = int(fields[2])
            except:
                return('error invalid message\n')
            subject,data = self.get_message(name,index)
            if not subject:
                return "error no such message for that user\n"
            response = "message %s %d\n" % (subject,len(data))
            response += data
            return response
        if fields[0] == 'store_key':
            try:
                name = fields[1]
                length = int(fields[2])
            except:
                return('error invalid message\n')
            key = self.read_put(length,fd)
            if not key:
                return('error invalid key\n')
            else:
                self.keys[name] = key
                return('OK\n')
        if fields[0] == 'get_key':
            try:
                name = fields[1]
            except:
                return('error invalid request\n')
            try:
                key = self.keys[name]
                logging.debug("KEY: %s" % key)
            except KeyError:
                return('error user doesn\'t exist\n')
            response = "key %i\n%s" % (len(key), key)
            return response
        return('error invalid message\n')
    
    def store_message(self,name,subject,data):
        if name not in self.messages:
            self.messages[name] = []
        self.messages[name].append((subject,data))

    def get_subjects(self,name):
        if name not in self.messages:
            return "",0
        response = ["%d %s\n" % (index+1,message[0]) for index,message in enumerate(self.messages[name])]
        return "".join(response),len(response)

    def get_message(self,name,index):
        if index <= 0:
            return None,None
        try:
            return self.messages[name][index-1]
        except:
            return None,None

    def read_put(self,length,fd):
        data = self.caches[fd]
        if len(data) > length:
            self.caches[fd] = data[length:]
            data = data[:length]
        else:
            self.caches[fd] = ''
        return data

    def send_response(self,response,fd):
        self.clients[fd].send(response)

def parse_options():
    parser = argparse.ArgumentParser(prog="Insecure encrypted chat server", description="chat server.", add_help=True)
    parser.add_argument("-d", "--debug", action="store_true", help="Turn on logging")
    parser.add_argument("-p", "--port", type=int, action="store", help="The port on which to host the server",default=1111)
    return parser.parse_args() 

if __name__ == '__main__':
    args = parse_options()
    logging.basicConfig(level=logging.DEBUG if args.debug else logging.ERROR)
    try:
        s = Server(args.port)
    except KeyboardInterrupt:
        logging.info("Exiting the server bruh.")
