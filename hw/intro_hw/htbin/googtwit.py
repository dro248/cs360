#!/usr/bin/env python

import bs4
import random
import requests
import threading

print "Content-type: text/html"
print
print "<h1>Headlines</h1>"

thingies = []

def getGoogle(url):
    news = requests.get(url).content
    soup = bs4.BeautifulSoup(news, 'html.parser')
    content = []
    for headline in soup.find_all('h2',{"class" :"esc-lead-article-title"}):
        content.append(headline)
    # then display the content
    y = ""
    y += "<div style='width:45%;float:left;'>"
    for x in content:
        y+=str(x)
    y += "</div>"
    thingies.append(y)

def getTwitter(url):
    news = requests.get(url).content
    soup = bs4.BeautifulSoup(news, 'html.parser')
    content = []
    for tweet in soup.find_all('p',{"class" :"tweet-text"}):
        content.append(tweet)
    # then display the content
    y = ""
    y+="<div style='width:45%;float:right;'>"
    for x in content:
        y+=str(x)
    y+="</div>"
    thingies.append(y)


def main():
    google = "http://news.google.com"
    twitter = "https://twitter.com/whatstrending"
    google_thread = threading.Thread(target=getGoogle,args=[google])
    twitter_thread = threading.Thread(target=getTwitter,args=[twitter])
    # start the threads
    google_thread.start()
    twitter_thread.start()
    google_thread.join()
    twitter_thread.join()
    for x in thingies:
        print x

if __name__ == "__main__":
    main(); 

