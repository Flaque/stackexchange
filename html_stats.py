from bs4 import BeautifulSoup

def stats(text):
    soup = BeautifulSoup(text, 'html.parser')

    totalTags = 0
    for tag in soup.findAll():
        totalTags += 1

    return totalTags
