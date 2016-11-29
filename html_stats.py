from bs4 import BeautifulSoup, SoupStrainer
import re

def tags(text):
    """ Returns total number of html tags in the text """
    soup = BeautifulSoup(text, 'html.parser')

    totalTags = 0
    for tag in soup.findAll():
        totalTags += 1

    return totalTags

def links(text):
    """ Returns number of links in text """
    links = SoupStrainer('a')
    return len([tag for tag in BeautifulSoup(text, 'html.parser',
        parse_only=links)])

def word_count(text):
    """ Returns the number of words in a piece of text """
    soup = BeautifulSoup(text, 'html.parser')
    dirty = soup.get_text() #Removes tags

    rx = re.compile('\W+')
    res = rx.sub(' ', dirty).strip() #Removes dirty chars `/`, `'`, `"`

    words = res.split(' ')
    return len(words)

test = """
<p>Is there any research/study/survey that looked at the main reasons why academics leave academia?</p>

<p>I did read <a href="http://theprofessorisin.com/its-ok-to-quit/" rel="nofollow">a</a> <a href="https://chroniclevitae.com/news/434-leaving-academia-it-s-time-to-have-the-talk" rel="nofollow">few</a> <a href="http://www.timeshighereducation.co.uk/news/id-have-to-be-mad-to-leave-here-they-said-and-they-were-right/420932.article" rel="nofollow">articles</a> <a href="http://chronicle.com/blogs/phd/2013/08/08/the-afternoon-i-decided-to-leave-academe-and-what-happened-next/" rel="nofollow">explaining</a> <a href="https://www.quora.com/Why-did-you-leave-academia?share=1" rel="nofollow">why</a> <a href="http://anothersb.blogspot.com/2014/02/goodbye-academia.html" rel="nofollow">some</a> <a href="http://thehairpin.com/2014/03/talking-to-anne-helen-petersen-about-why-shes-leaving-academia-for-buzzfeed" rel="nofollow">particular</a> <a href="http://blog.devicerandom.org/2011/02/18/getting-a-life/" rel="nofollow">academics</a> <a href="http://lilligroup.com/tag/deciding-to-leave-academia-when-it-was-your-dream-profession/" rel="nofollow">left</a> <a href="http://crypto.junod.info/2013/09/09/an-aspiring-scientists-frustration-with-modern-day-academia-a-resignation/" rel="nofollow">academia</a>, but I would like to have some statistics to see what are the most common reasons invoked.</p>

<p>I mostly interested in the computer science field (machine learning) in the US, but curious about other fields and locations as well.</p>

"""
