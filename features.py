from spacy.en import English
import html_stats as html
parser = English()

def answer(question, answer):
    """ Gets features for the answer """

    # Compute HTML features first
    link_ratio = html.link_ratio(answer)
    tag_ratio = html.tag_ratio(answer)

    # Spacy doesn't like non-unicode inputs
    question = unicode(question)
    answer = unicode(answer)

    # Parse out the question and answer
    question_doc = parser(question)
    answer_doc = parser(answer)

    # Compute NLP features
    similarity = answer_doc.similarity(question_doc)
    entities = len(list(answer_doc.ents))
    sentences = len(list(answer_doc.sents))

    # Return a dictionary of features
    return {
        'similarity' : similarity,
        'entities'   : entities,
        'sentences'  : sentences,
        'link_ratio' : link_ratio,
        'tag_ratio'  : tag_ratio
    }
