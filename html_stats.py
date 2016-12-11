from bs4 import BeautifulSoup, SoupStrainer
import re

def tags(text):
    """ Returns total number of html tags in the text """
    soup = BeautifulSoup(text, 'html.parser')

    totalTags = 0
    for tag in soup.findAll():
        totalTags += 1

    return totalTags

def tag_ratio(text):
    return tags(text) / (len(text) * 1.0)

def links(text):
    """ Returns number of links in text """
    links = SoupStrainer('a')
    return len([tag for tag in BeautifulSoup(text, 'html.parser',
        parse_only=links)])

def link_ratio(text):
    return links(text) / (len(text) * 1.0)

def word_count(text):
    """ Returns the number of words in a piece of text """
    soup = BeautifulSoup(text, 'html.parser')
    dirty = soup.get_text() #Removes tags

    rx = re.compile('\W+')
    res = rx.sub(' ', dirty).strip() #Removes dirty chars `/`, `'`, `"`

    words = res.split(' ')
    return len(words)
