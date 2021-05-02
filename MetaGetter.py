import json
import sys

from bs4 import BeautifulSoup
from os import listdir
import os
import re
from os.path import isfile, join

path = 'korpus/'
inverted_index = {}
count = 0

def tokenize(corpus):
    autoSaveCount=0
    for file in corpus:
        filename = os.path.abspath(path + file)
        content = open(filename, mode='r', encoding='utf-8').read()
        content = re.split('--------', content)[1]
        for token in re.split('[\s.,!?]', content):
            if token is not '':
                i = token.strip().lower()
                if inverted_index.get(i) is None:
                    inverted_index[i] = 1
                else:
                    inverted_index[i] += 1
        autoSaveCount+=1
        if autoSaveCount>=20:
            autoSave()
            autoSaveCount=0

def autoSave():
    with open('data.json', 'w',  encoding='utf-8') as fp:
        json.dump(inverted_index, fp, ensure_ascii=False)
        print('saved file')

def countWords():
    value = 0
    for i in inverted_index.values():
        value+=i
    print('Einzigartige Wörter: ' + str(len(inverted_index.keys())))
    print('Alle Wörter: ' + str(value))


def getMetaData(corpus):
    tokenize(corpus)
    countWords()


if __name__ == '__main__':
    corpus = [f for f in listdir(path) if isfile(join(path, f))]
    getMetaData(corpus)