import random
import re
import requests
from time import sleep
from bs4 import BeautifulSoup

speaker_list = []

speeches_List = []
pattern = re.compile('DE.*.html')

def doScrape():
    r = requests.session()
    r.headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36'}
    for speaker in speaker_list:
        new_content = r.get(speaker).text
        forward = []
        while forward is not None:
            content = new_content
            soup = BeautifulSoup(content)
            for element in soup.find_all('a', href=True):
                if element.parent.name == 'h4':
                    print("Found Speech:", element['href'])
                    c = r.get(element['href']).text
                    name = re.split(';', element['href'])[0].replace('/','_')
                    with open(name +".txt", "w", encoding="utf-8") as saveFile:
                        saveFile.write(c)
                    sleepTimer = random.uniform(3, 12)
                    print("Sleeping for: ", sleepTimer, "s")
                    sleep(sleepTimer)
            sleepTimer = random.randint(30, 180)
            print("Sleeping for: ", sleepTimer, "s")
            sleep(sleepTimer)
            forward = soup.find('li', attrs={'class': 'forward'})
            if forward is not None:
                print("Next:", forward.findChild('a')['href'])
                new_content = r.get(forward.findChild('a')['href']).text


if __name__ == '__main__':
    doScrape()
