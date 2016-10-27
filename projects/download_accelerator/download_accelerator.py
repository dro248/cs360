#!/usr/bin/env python

import threading
import sys, logging
import argparse
import re

class Download_Manager():
    """ handles the threading and organizing for a download """
    def __init__(self,num_threads,url):
        self.threads = []
    def get_content_length():
        """ Makes a HEAD request to the url's web server for the Content-Length """
    def manage():
        """ The main logic for the downloader """
    def make_threads():
        """ Makes the threads for the download """
    def download():
        """ Creates the threads and downloads the file. Then it """
    def assemble():
        """ Puts the downloaded content back together again """

def parse_options():
    parser = argparse.ArgumentParser(prog="Download Accelerator", description="Threaded Static File Downloader", add_help=True)
    parser.add_argument("-n", "--number", type=int, action="store", help="Specify the number of threads to create",default=10)
    parser.add_argument("-d", "--debug", action="store_true", help="Turn on logging")
    return parser.parse_args() 

def isUrl(string):
    """ Check to see if this is the url param
    It's not important to check for more than just http 
    because this is the only param that we will need to check """
    return True if string.startswith("http") else False

def get_url():
    logging.debug("Getting the URL")
    logging.debug(sys.argv)

if __name__ == "__main__":
    args = parse_options()
    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)
    num_threads = args.number if args.number > 0 else 1
    logging.debug("number of threads %d" % num_threads)
    get_url()
    dlmngr = Download_Manager(args.url, num_threads=num_threads)

