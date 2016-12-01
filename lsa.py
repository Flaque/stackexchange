import operator
import re

def term_frequency(term, document):
    dictionary = {}
    for term in document.split(' '):
        try:
            dictionary[term] += 1
        except KeyError:
            dictionary[term] = 1
    return dictionary

def appearances(term, documents):
    count = 0
    for d in documents:
        if term in d:
            count += 1
    return count

def inverse_document_frequency(term, documents):
    return len(documents) / ((1 + abs(appearances(term, documents))) * 1.0)

def id_idf(term, document, documents):
    freqs = term_frequency(term, document)
    return freqs[term] * inverse_document_frequency(term, documents)

def weight_vector(document, documents):
    return [id_idf(term, document, documents) for term in document.split(' ')]

def sim(document, query):
    both = [document, query]
    document_vector = weight_vector(document, both)
    query_vector = weight_vector(query, both)
    zipped_vectors = zip(document_vector, query_vector)

    top = sum([ d*q for d, q in zipped_vectors])
    bot = sum([ d**2 for d in document_vector]) * sum([ q**2 for q in query_vector])
    return top / (bot * 1.0)

def strip_text(text):
    rx = re.compile('\W+')
    return rx.sub(' ', text).strip()

def parse_documents(corpus_file):
    documents = []
    for line in corpus_file:
        documents.append(strip_text(line))
    return documents

def split_sentences(text):
    sentences = re.split(r' *[\.\?!][\'"\)\]]* *', text)
    stripped = [s.strip() for s in sentences]

    returnable = []
    for s in stripped:
        if s:
            returnable.append(s)
    return returnable

def main():
    k = 10

    with open('doc.md', 'r') as _corpus:
        text = ''.join(_corpus.readlines())
        sentences = split_sentences(text)

        sims = []
        for i in range(0, len(sentences)-1):
            for j in range(i, len(sentences)):
                sim_val = sim(sentences[i], sentences[j])

                sims.append(((i, j, sentences[i], sentences[j]), sim_val))

        length = len(sims)
        sims_sorted = sorted(sims, key=operator.itemgetter(1))

        for i in range(0, k):
            del sims_sorted[-1]

        new_text = [''] * length
        for sentence, value in sims_sorted:
            i, j, sen_1, sen_2 = sentence
            new_text[i] = sen_1 + '. \n'


        print ''.join(new_text)

    # with open('test_corpus.txt', 'r') as _corpus:
    #     documents = parse_documents(_corpus)
    #
    #     sims = []
    #     for i in range(0, len(documents)):
    #         for j in range(i, len(documents)):
    #             sims.append(sim(documents[i], documents[j]))
    #
    #     print sorted(sims)

main()
