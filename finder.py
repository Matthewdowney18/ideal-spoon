from urllib.request import urlopen
import re
from bs4 import BeautifulSoup
from nltk import word_tokenize

#only using one sample book for testing purposes
sample = ['_001', 'y', 'fiction_SS', 'black_eyed_susan.txt', 'Joseph Devon', 'Black Eyed Susan']

#finds the last initial of the author
def getlastinitial(info):
    names = word_tokenize(info[4])
    lastinitial = names[-1][0].lower()
    return lastinitial

#gets the first name of the author
def getfirstname(info):
    names = word_tokenize(info[4])
    firstname = names[0].lower()
    return firstname

#goes into the page with the list of authors
src = urlopen('http://manybooks.net/authors.php?alpha=' + getlastinitial(sample))
soup = BeautifulSoup(src, "html.parser")

#creating a list of links
links=[]
for link in soup.find_all('a'):
    links.append(link.get('href'))

#trying to find the author(dosent work quite yet)
for i in range(0,len(links)):
    searchObj = re.search(r'(joseph)', links[i], re.M | re.I)
    if searchObj:
        link = i
        break;

print(links[link])
