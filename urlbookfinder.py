import csv
from urllib.request import urlopen
import re
from bs4 import BeautifulSoup
from nltk import word_tokenize


# finds the last initial of the author
def get_last_initial(info):
    names = word_tokenize(info[4])
    last_initial = names[-1][0].lower()
    return last_initial


# gets the first name of the author
def get_first_name(info):
    names = word_tokenize(info[4])
    last_first_name = names[-1].lower()+', '+names[0]
    return last_first_name


# finds the links on the page, then finds the specific link that were loking for
def link_finder(soup, book_info):
    # creating list of links, with the name tags in them
    links = []
    for a in soup.find_all('a'):
        links.append(str(a))

    link = 'none'
    # trying to find the author
    for i in range(0, len(links)):
        search_obj = re.search(book_info, links[i], re.M | re.I)
        if search_obj:
            link = links[i]
            break
    return link


# finds the file name for the url inside the link
def file_finder(link):
    file = ''
    i = link.find("href=") + 6
    while link[i] != '"':
        file += link[i]
        i += 1
    return file


# read the csv
with open('fiction_sources.csv', 'r')as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')

    for line in reader:
        # goes into the page with the list of authors with that last name
        src = urlopen('http://manybooks.net' + '/authors.php?alpha=' + get_last_initial(line))
        soup = BeautifulSoup(src, "html.parser")

        author = get_first_name(line)
        authorlink = link_finder(soup, author)
        # error check
        if authorlink == 'none':
            print('none')
            continue
        # find the file name
        authorFileName = file_finder(authorlink)

        # going to the authors page
        src = urlopen('http://manybooks.net' + authorFileName)
        soup = BeautifulSoup(src, "html.parser")

        book_link = link_finder(soup, line[5])
        # error check
        if book_link == 'none':
            print('none')
            writer.writerow(line.append('none'))
            continue
        # find the file name
        bookFileName = file_finder(book_link)

        # finding the final link to the book,this stage takes the longest by far
        src = urlopen('http://manybooks.net' + bookFileName)
        soup = BeautifulSoup(src, "html.parser")
        final_book_link = link_finder(soup, 'read online in browser here')
        final_book_url = 'http://manybooks.net' + file_finder(final_book_link)
        print(final_book_url)
        # figure out how to write a new csv

