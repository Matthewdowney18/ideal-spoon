import csv
from urllib.request import urlopen
import re
from bs4 import BeautifulSoup
from nltk import word_tokenize


#finds the last initial of the author
def getlastinitial(info):
    names = word_tokenize(info[4])
    lastinitial = names[-1][0].lower()
    return lastinitial

#gets the first name of the author
def getfirstname(info):
    names = word_tokenize(info[4])
    lastfirstname = names[-1].lower()+', '+names[0]
    return lastfirstname

#finds the links on the page, then finds the specific link that were loking for
def linkfinder(soup, bookinfo):
    # creating list of links, with the name tags in them
    links = []
    for a in soup.find_all('a'):
        links.append(str(a))

    link = 'none'
    # trying to find the author
    for i in range(0, len(links)):
        searchObj = re.search(bookinfo, links[i], re.M | re.I)
        if searchObj:
            link = links[i]
            break

    return link

#finds the file name for the url inside the link
def filefinder(link):
    file=''
    i = link.find("href=")+ 6
    while link[i] != '"':
        file+= link[i]
        i+=1
    return file

with open('fiction_sources.csv', 'r')as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')

    with open('fiction_sources2.csv', 'w')as newfile:
        writer = csv.writer(newfile, delimiter=',')

        for line in reader:

            # goes into the page with the list of authors with that last name
            src = urlopen('http://manybooks.net' + '/authors.php?alpha=' + getlastinitial(line))
            soup = BeautifulSoup(src, "html.parser")

            author = getfirstname(line)
            authorlink = linkfinder(soup, author)
            #error check
            if authorlink == 'none':
                print('none')
                continue
            #find the file name
            authorFileName = filefinder(authorlink)

            # going to the authors page
            src = urlopen('http://manybooks.net' + authorFileName)
            soup = BeautifulSoup(src, "html.parser")

            booklink = linkfinder(soup, line[5])
            # error check
            if booklink == 'none':
                print('none')
                writer.writerow(line.append('none'))
                continue
            #find the file name
            bookFileName = filefinder(booklink)


            # finding the final link to the book, this stage takes the longest by far
            src = urlopen('http://manybooks.net' + bookFileName)
            soup = BeautifulSoup(src, "html.parser")
            finalbooklink = linkfinder(soup, 'read online in browser here')
            finalbookurl = 'http://manybooks.net' + filefinder(finalbooklink)
            print(finalbookurl)
            #figure out how to write a new csv

