#!/usr/bin/env python

import bs4
import random
import requests

print "Content-type: text/html"
print
print "<h1>Headlines</h1>"

news = requests.get("http://news.google.com").content
soup = bs4.BeautifulSoup(news, 'html.parser')
for headline in soup.find_all('h2',{"class" :"esc-lead-article-title"}):
    print headline
