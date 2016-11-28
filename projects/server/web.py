#!/usr/bin/env python

import argparse
import logging

from server import Server

class Main():
    def __init__(self):
        self.args = self.parse_args()
        self.configure_logging()

    def parse_args(self):
        parser = argparse.ArgumentParser(prog="server", description="serves files, yo", add_help=True)
        parser.add_argument("-p", "--port", action="store", type=int, help="the port, dude", default=1111)
        parser.add_argument("-d", "--debug", action="store true", help="do you want debugging, mang?")
        return parser.parse_args()

    def configure_logging(self):
        if self.args.debug:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.ERROR)

    def parse_config(self):
       # parse the config file, mate 

if __name__ == "__main__":
    m = Main()

