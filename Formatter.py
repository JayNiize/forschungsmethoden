from bs4 import BeautifulSoup
from os import listdir
import os
import re
from os.path import isfile, join

path = "korpus_raw/"
path_to_save = "korpus/"


def doFormat():
    crawled_files = [f for f in listdir(path) if isfile(join(path, f))]
    for file in crawled_files:
        extractContent(file)
    print("finished")


def extractContent(file):
    try:
        content = open(os.path.abspath(path + file), encoding="utf-8", mode="r").read()
        soup = BeautifulSoup(content)
        content = soupContent(soup)
        if content is None:
            raise AttributeError

        speech_date_and_place = soupDate(soup)
        if speech_date_and_place is None:
            speech_date_and_place = ""

        output = speech_date_and_place + "\n--------\n" + content
        saveFile(file, output)

    except AttributeError:
        print("Attribute Error on File: " + file)


def soupDate(soup):
    if soup.find('span', attrs={'class': 'date'}) is not None:
        return soup.find('span', attrs={'class': 'date'}).text

    if soup.find('div', attrs={'class': 'article-metadata'}) is not None:
        return soup.find('div', attrs={'class': 'article-metadata'}).text
    return None


def soupContent(soup):
    for div in soup.find_all('div', {'class': None, 'id': None}):
        try:
            if div.parent.attrs['id'] == 'main-inner':
                return div.text
        except KeyError:
            continue
    print('Error - no main-inner found')
    return None


def saveFile(file, content):
    filename = file.replace('.html', '').replace('SharedDocs_', '')
    with open(path_to_save + filename, "w", encoding="utf-8") as saveFile:
        saveFile.write(content)
        print('saved file:' + filename)


if __name__ == "__main__":
    doFormat()
