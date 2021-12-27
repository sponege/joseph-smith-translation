#!/usr/bin/env python3
## This script automatically finds malicious/unwanted packages on a Linux system, asks if the package should be removed, and removes them.
## Written by Jordan Perry, 12/22/2021
import os
import time
import subprocess
import re
# os.system("sudo apt install python3-pip")
# os.system("pip install beautifulsoup4")

from bs4 import BeautifulSoup
from requests import get

start_time = time.time()

usr_agent = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/61.0.3163.100 Safari/537.36"}

ot = [["gen", 50], ["ex", 40], ["lev", 27], ["num", 36], ["deut", 34], ["josh", 24], ["judg", 21], ["ruth", 4], ["1-sam", 31], ["2-sam", 24], ["1-kgs", 22], ["2-kgs", 25], ["1-chr", 29], ["2-chr", 36], ["ezra", 10], ["neh", 13], ["esth", 10], ["job", 42], ["ps", 150], ["prov", 31], ["eccl", 12], ["song", 8], ["isa", 66], ["jer", 52], ["lam", 5], ["ezek", 48], ["dan", 12], ["hosea", 14], ["joel", 3], ["amos", 9], ["obad", 1], ["jonah", 4], ["micah", 7], ["nahum", 3], ["hab", 3], ["zeph", 3], ["hag", 2], ["zech", 14], ["mal", 4]]

def fetch_address(url):

    proxies = {"http":None}
    while True:
        try:
            response = get(url, headers=usr_agent, proxies=proxies)
            response.raise_for_status()
            break
        except:
            print("!!! Link cannot be reached! Retrying... !!!")

    return str(response.content, encoding='utf-8', errors='ignore')

# verses = fetch_scripture("ot", "gen", "1")
# print(verses[0])
# print(verses[1])

website = "http://stewartonbibleschool.org/bible/text/"
soup = BeautifulSoup(fetch_address(website), "html.parser")
bible = open("bible-kjv.txt", "a+")
for link in soup.find_all('a')[1:-3]:
    # book = book.replace("\n", f"{re.find("([A-Z])\n1:1")})
    book = fetch_address(f"{website}{link['href']}")
    book = book.strip()
    book = re.sub(r"\n\n", r"\n", book)
    book = '\n'.join([verse.strip() for verse in book.split('\n')])
    title = re.search("([A-Z]+)(.+)\n1:1", book).group(0).split('\n')[0].title()
    book = f"{title} {book[book.lower().find(title.lower())+len(title)+1:]}"
    book = re.sub(r"\n", f"\n{title} ", book)
    book = re.sub(r"([0-9]): ", r"\1\t", book)
    print(book)
    bible.write(book)
    bible.write('\n')
bible.close()

print(f"It took {time.time() - start_time} seconds to download the entire King James Version of the Old and New Testament")
