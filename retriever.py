import indexer
from stemming.porter2 import stem
import nltk


def get_pages(search_query):
    index = indexer.construct_index('indices/index_1.txt')
    search_query = nltk.word_tokenize(search_query)
    search_query = [stem(word.lower()) for word in search_query]
    print search_query
    pages = set(index.get(search_query[0]))
    for i in xrange(1, len(search_query)):
        word = search_query[i]
        pages = pages.intersection(set(index.get(word)))
    return list(pages)

if __name__ == '__main__':
    pages = get_pages('Djokovic Nadal')
    print pages
