import re
import math


def ARI(characters, words, sentences):
    """ Calculates the Automated Reading Index """
    return 4.71*(characters/words) + 0.5*(words/sentences) - 21.43

def grade_level(text):
    characters = len(text)
    words = len(text.split(' '))
    sentences = len(re.split(r' *[\.\?!][\'"\)\]]* *', text))

    return int(math.ceil(ARI(characters,words,sentences)))

my_text = "The rule of rhythm in prose is not so intricate. Here, too, we write in groups, or phrases, as I prefer to call them, for the prose phrase is greatly longer and is much more nonchalantly uttered than the group in verse; so that not only is there a greater interval of continuous sound between the pauses, but, for that very reason, word is linked more readily to word by a more summary enunciation. Still, the phrase is the strict analogue of the group, and successive phrases, like successive groups, must differ openly in length and rhythm. The rule of scansion in verse is to suggest no measure but the one in hand; in prose, to suggest no measure at all. Prose must be rhythmical, and it may be as much so as you will; but it must not be metrical. It may be anything, but it must not be verse. "
print(grade_level(my_text))
