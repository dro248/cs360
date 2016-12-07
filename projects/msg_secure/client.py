from Crypto.PublicKey import RSA
from Crypto import Random
import fileinput
import optparse
import socket
import sys

import argparse
import logging

class Client:
    def __init__(self,host,port):
        self.host = host
        self.port = port
        self.server = None
        self.cache = ''
        self.messages = {}
        self.key = None
        self.name = ''
        self.size = 10024
        self.open_socket()
        self.run()

    def open_socket(self):
        """ Connect to the server """
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.connect((self.host,self.port))
        except socket.error, (value,message):
            if self.server:
                self.server.close()
            print "Could not connect to server: " + message
            sys.exit(1)

    def run(self):
        while True:
            # get input from users
            self.prompt()
            command = sys.stdin.readline()
            result = self.parse_command(command)
            if not result:
                print "I don't recognize that command."

    ### Interaction with user ###

    def prompt(self):
        sys.stdout.write("% ")

    def parse_command(self,command):
        fields = command.split()
        if not fields:
            return('error invalid message\n')
        if fields[0] == 'quit':
            sys.exit()
        if fields[0] == 'send':
            ### send message ###
            try:
                name = fields[1]
                subject = fields[2]
            except:
                return False
            data = self.get_user_message()
            key = self.get_key(name)
            data = key.publickey().encrypt(data, 0)[0]
            print "The encrypted data:",data
            self.send_put(name,subject,data)
            self.response_to_put()
            return True
        if fields[0] == 'list':
            ### list messages ###
            try:
                name = fields[1]
            except:
                return False
            self.send_list(name)
            self.response_to_list()
            return True
        if fields[0] == 'read':
            ### read message ###
            try:
                name = fields[1]
                index = int(fields[2])
            except:
                return False
            self.send_read(name,index)
            self.response_to_read()
            return True
        if fields[0] == 'login':
            try:
                self.name = fields[1]
            except:
                return False
            self.gen_key_pair()
            self.send_login(self.key.publickey().exportKey())
            self.response_to_login()
            return True
        return False

    ### Generic message handling ###

    def get_response(self):
        # get a response from the server
        while True:
            data = self.server.recv(self.size)
            if not data:
                print "Connection to server closed."
                sys.exit()
            self.cache += data
            message = self.read_message()
            if not message:
                continue
            return message

    def read_message(self):
        # read until we have a newline and store excess in cache
        index = self.cache.find("\n")
        if index == "-1":
            return None
        message = self.cache[0:index+1]
        self.cache = self.cache[index+1:]
        return message

    def send_request(self,request):
        self.server.sendall(request)

    ### Handling login ###
    
    def send_login(self,pub_key):
        """ Pub key should be the exported text version """
        self.send_request("store_key %s %i\n%s" % (self.name, len(pub_key), pub_key))

    def gen_key_pair(self):
        random_generator = Random.new().read
        self.key = RSA.generate(2048, random_generator)

    def response_to_login(self):
        message = self.get_response()
        if message != "OK\n":
            print "Server returned bad message:",message
            return

    ### Handling encryption ###

    def get_key(self, name):
        self.send_request("get_key %s\n" % name)
        message = self.get_response()
        fields = message.split()
        try:
            if fields[0] != 'key':
                print "server returned bad message:", message
                return
            length = int(fields[1])
        except:
            print "server returned bad message",message
            return 
        pub_key = self.get_key_response(length)
        return RSA.importKey(pub_key)

    def get_key_response(self,length):
        data = self.cache
        while len(data) < length:
            d = self.server.recv(self.size)
            if not d:
                self.cache = ''
                logging.info("Server did not send the whole message: %s"%data)
                return None
            data += d
        if data > length:
            self.cache = data[length:]
            data = data[:length]
        else:
            self.cache = ''
        return data

    ### Handling send ###

    def send_put(self,name,subject,data):
        self.send_request("put %s %s %d\n%s" % (name, subject, len(data), data))

    def get_user_message(self):
        print "- Type your message. End with a blank line -"
        message = ""
        while True:
            # get input from user
            data = sys.stdin.readline()
            if data == "\n":
                return message
            message += data

    def response_to_put(self):
        message = self.get_response()
        if message != "OK\n":
            print "Server returned bad message:",message
            return

    ### Handling list ###

    def send_list(self,name):
        self.send_request("list %s\n" % name)

    def response_to_list(self):
        message = self.get_response()
        fields = message.split()
        try:
            if fields[0] != 'list':
                print "Server returned bad message:",message
                return
            num = int(fields[1])
        except:
            print "Server returned bad message:",message
            return
        self.read_list_response(num)


    def read_list_response(self,num):
        total = 0
        while (total < num):
            data = self.read_message()
            print data,
            total += 1

    ### Handling read ###

    def send_read(self,name,index):
        self.send_request("get %s %s\n" % (name, index))

    def response_to_read(self):
        message = self.get_response()
        fields = message.split()
        try:
            if fields[0] != 'message':
                print "Server returned bad message:",message
                return
            subject = fields[1]
            length = int(fields[2])
        except:
            print "Server returned bad message:",message
            return
        self.read_message_response(subject,length)

    def read_message_response(self,subject,length):
        data = self.cache
        while len(data) < length:
            d = self.server.recv(self.size)
            if not d:
                self.cache = ''
                print "Server did not send the whole message:",data
                return None
            data += d
        if data > length:
            self.cache = data[length:]
            data = data[:length]
        else:
            self.cache = ''
        print subject
        print data,

def parse_options():
    parser = argparse.ArgumentParser(prog="Insecure encrypted chat server", description="chat server.", add_help=True)
    parser.add_argument("-d", "--debug", action="store_true", help="Turn on logging")
    parser.add_argument("-p", "--port", type=int, action="store", help="The port on which to host the server",default=1111)
    return parser.parse_args() 

if __name__ == '__main__':
    args = parse_options()
    logging.basicConfig(level=logging.DEBUG if args.debug else logging.ERROR)
    try:
        s = Client('localhost',args.port)
    except KeyboardInterrupt:
        logging.info("Exiting, son.")

