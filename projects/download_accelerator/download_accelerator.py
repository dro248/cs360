#!/usr/bin/env python

import threading
import sys, logging
import argparse
import requests
from urlparse import urlparse
import time

class Dl_Range(threading.Thread):
    """ The worker Thread functionality """
    def __init__(self,url,dl_range):
        threading.Thread.__init__(self)
        self.url = url
        if dl_range[0] >= dl_range[1] or dl_range[0] < 0:
            logging.error("Invalid range given: %d-%d" % (dl_range[0], dl_range[1]))
            self.range = None
        else:
            logging.debug("Range set to: %d-%d" % (dl_range[0], dl_range[1]))
            self.range = dl_range

    def run(self):
        """ Download the range that is specified """
        self.get_content(self.gen_headers())

    def get_content(self, headers):
        """ Makes the GET request to get the range of content that was specified """
        r = requests.get(self.url, headers=headers)
        self.content = r.content

    def gen_headers(self):
        if self.range is None:
            logging.error("Range has not been defined")
        else:
            headers = {}
            headers["Accept-Encoding"] = "identity"
            headers["Range"] = "bytes=%d-%d" % self.range
            logging.debug("headers: %s" % str(headers))
            return headers

class Download_Manager():
    """ handles the threading and organization of a download """
    def __init__(self,num_threads,url):
        self._threads = []
        self._content_length = 0
        self._url = url
        self._num_threads = num_threads
        self._end_time = 0.0
        self._start_time = 0.0
        self._dl_success = False
        self.manage()

    def real_url(self):
        url = urlparse(self._url)
        if url.scheme is "" or url.hostname is "":
            logging.error("Url is bad: %s" % self._url)
            return False
        else:
            logging.debug("Url is good: %s" % self._url)
            return True

    def get_content_length(self):
        """ Makes a HEAD request to the url's web server for the Content-Length """
        head = requests.head(self._url, headers={"Accept-Encoding":"identity"})
        try:    
            self._content_length = int(head.headers["Content-Length"])
            logging.debug("Content-Length: %s" % self._content_length)
        except:
            logging.error("No content Length Header is set. Cannot download.")

    def manage(self):
        """ The main logic for the downloader """
        if not self.real_url():
            logging.error("Exiting manage.")
            return
        self.get_content_length()
        if self._content_length is 0:
            logging.error("Content-Length header not set. Non-Static site. Download Failed.")
            return
        else:
            self.make_threads()
            self.download()
            self.write_to_file()
            
    def gen_ranges(self):
        """ Generates the ranges = Array(Tuple()) """
        range_length = self._content_length // self._num_threads
        if range_length > 0:
            ranges = []
            prev_end = -1
            for x in xrange(0,self._num_threads):
                beg = prev_end + 1
                prev_end += range_length
                end = prev_end
                if x is self._num_threads-1:
                    if end < self._content_length:
                        logging.debug("Final Range before: %d, after: %d" % (end,self._content_length))
                        end = self._content_length
                ranges.append((beg,end))
            return ranges
        else:
            logging.critical("More threads specified than bytes in download.\nExiting.")
            sys.exit(1)

    def make_threads(self):
        """ Makes the threads for the download """
        ranges = self.gen_ranges()
        self._start_time = float(time.time())*1000
        for dl_range in ranges:
            self._threads.append(Dl_Range(self._url,dl_range))

    def download(self):
        """ starts all of the threads """
        for thread in self._threads:
            thread.start()
        for thread in self._threads:
            thread.join()
        self._end_time = float(time.time())*1000

    def write_to_file(self):
        """ Puts the downloaded content back together again """
        path = urlparse(self._url).path
        logging.debug(path)
        if path is not "":
            filename = path.split("/")[-1]
            filename = filename if len(filename) > 0 else "index.html"
        else:
            filename = "index.html"
        logging.info("writing to %s" % filename)
        with open(filename, "w") as dl_file:
            for thread in self._threads:
                dl_file.write(thread.content)
        self._dl_success = True

    def get_stats(self):
        if not self._dl_success:
            logging.info("Download Failed")
            return "Download Failed"
        stats = "[%s] [%s] [%d] [%f]" % (self._url, self._num_threads, self._content_length, (self._end_time-self._start_time)/1000)
        return stats

def parse_options():
    parser = argparse.ArgumentParser(prog="Download Accelerator", description="Threaded Static File Downloader", add_help=True)
    parser.add_argument("-d", "--debug", action="store_true", help="Turn on logging")
    parser.add_argument("-n", "--number", type=int, action="store", help="Specify the number of threads to create",default=1)
    parser.add_argument("url", help="The url of the page that you want to download")
    return parser.parse_args() 

if __name__ == "__main__":
    args = parse_options()
    logging.basicConfig(level=logging.DEBUG if args.debug else logging.ERROR)
    num_threads = args.number if args.number > 0 else 1
    dlmgr = Download_Manager(num_threads=num_threads, url=args.url)
    print(dlmgr.get_stats())


