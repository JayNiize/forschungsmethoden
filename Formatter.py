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
        try:
            content = open(os.path.abspath(path+file), encoding="utf-8", mode="r").read()
            content = re.split("(caption-wrapper|sectionRelated)", content)
            soup = BeautifulSoup(content[2])
            speech_date_and_place_raw = soup.find('span', attrs={'class':'date'})
            speech_date_and_place = ""
            if speech_date_and_place_raw is not None:
                speech_date_and_place = speech_date_and_place_raw.text
            speech_content = soup.find('div', attrs={'class':None}).text

            output = speech_date_and_place + "\n\n"+ speech_content
            filename = file.replace('.html','').replace('SharedDocs_','')
            with open(path_to_save+ filename, "w", encoding="utf-8") as saveFile:
                saveFile.write(output)

        except AttributeError:
            print("Attribute Error on File: "+ file)

    print("finished")




if __name__ == "__main__":
    doFormat()
