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
nt = [["matt", 28], ["mark", 16], ["luke", 24], ["john", 21], ["acts", 28], ["rom", 16], ["1-cor", 16], ["2-cor", 13], ["gal", 6], ["eph", 6], ["philip", 4], ["col", 4], ["1-thes", 5], ["2-thes", 3], ["1-tim", 6], ["2-tim", 4], ["titus", 3], ["philem", 1], ["heb", 13], ["james", 5], ["1-pet", 5], ["2-pet", 3], ["1-jn", 5], ["2-jn", 1], ["3-jn", 1], ["jude", 1], ["rev", 22]]
bofm = [["1-ne", 22], ["2-ne", 33], ["jacob", 7], ["enos", 1], ["jarom", 1], ["omni", 1 ], ["w-of-m", 1], ["mosiah", 29], ["alma", 63], ["hel", 16], ["3-ne", 30], ["4-ne", 1], ["morm", 9], ["ether", 15], ["moro", 10]]
pgp = [["moses", 8], ["abr", 5], ["js-m", 1], ["a-of-f", 1]]
dc = [["dc", 138]]
def fetch_scripture(division, book, chapter):

    url = f"https://www.churchofjesuschrist.org/study/scriptures/{division}/{book}/{chapter}"
    ## example: https://www.churchofjesuschrist.org/study/scriptures/ot/gen/1
    proxies = {"http":None}
    while True:
        try:
            response = get(url, headers=usr_agent, proxies=proxies)
            response.raise_for_status()
            break
        except:
            print("!!! ChurchOfJesusChrist.org cannot be reached! Retrying... !!!")

    soup = BeautifulSoup(str(response.content, encoding='utf-8', errors='ignore'), "html.parser")

    chapter = soup.find('span', attrs={"class": re.compile("toTopLink(.+)")}).getText()
    summary = soup.find('p', attrs={"class": "study-summary"}).getText()
    # summary = summary.replace('â', '—')
    for footnote in soup.find_all('sup', attrs={"class": "marker"}):
        footnote.decompose()
    for number in soup.find_all('span', attrs={"class": "verse-number"}):
        number = number.replaceWith('\n')
    verses = soup.find("div", attrs={"class": "body-block"})
    verses = verses.getText().replace('¶', '').split('\n')
    for i in range(len(verses)):
        verses[i] = verses[i].strip()
        verses[i] = f"{chapter}:{i}\t{verses[i]}"
    verses = verses[1:]
    verses = '\n'.join(verses)
    summary = f"{chapter}\t{summary}"
    return (verses, summary)
    # print(verses.getText()) ## link["href"], having the url was just way too goddamn annoying

# verses = fetch_scripture("ot", "gen", "1")
# print(verses[0])
# print(verses[1])

# bible = open("bible-jst.txt", "a+")
# summary = open("bible-summaries.txt", "a+")
#
# for book in ot:
#     for i in range(1, book[1] + 1):
#         verses, summ = fetch_scripture("ot", book[0], i)
#         print(summ)
#         bible.write(verses)
#         bible.write('\n')
#         summary.write(summ)
#
# for book in nt:
#     for i in range(1, book[1] + 1):
#         verses, summ = fetch_scripture("nt", book[0], i)
#         print(summ)
#         bible.write(verses)
#         bible.write('\n')
#         summary.write(summ)


# bible = open("bofm.txt", "a+")
# summary = open("bofm-summaries.txt", "a+")
#
# for book in bofm:
#     for i in range(1, book[1] + 1):
#         verses, summ = fetch_scripture("bofm", book[0], i)
#         print(summ)
#         bible.write(verses)
#         bible.write('\n')
#         summary.write(summ)
#         summary.write('\n')

# bible = open("pgp.txt", "a+")
# summary = open("pgp-summaries.txt", "a+")
#
# for book in pgp:
#     for i in range(1, book[1] + 1):
#         verses, summ = fetch_scripture("pgp", book[0], i)
#         print(summ)
#         bible.write(verses)
#         bible.write('\n')
#         summary.write(summ)
#         summary.write('\n')

bible = open("dc.txt", "a+")
summary = open("dc-summaries.txt", "a+")

for book in dc:
    for i in range(1, book[1] + 1):
        verses, summ = fetch_scripture("dc-testament", book[0], i)
        print(summ)
        bible.write(verses)
        bible.write('\n')
        summary.write(summ)
        summary.write('\n')

bible.close()
summary.close()
print(f"It took {time.time() - start_time} seconds to download the entire Pearl of Great Price")
