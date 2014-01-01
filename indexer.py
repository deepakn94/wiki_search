# TODO: Need to add positional information and reverse index
# construction
# Also need to handle punctuation (may come under stemming)

from collections import defaultdict
from stemming.porter2 import stem

stop_words = ['this', 'the']
reverse_index = defaultdict(list)


def parse_document(text):
    tokens = text.split()
    return [stem(token.lower()) for token in tokens if token not in stop_words]


def construct_reverse_index(tokens, url):
    i = 0
    global reverse_index
    for token in tokens:
        reverse_index[token].append((i, url))
        i += 1

if __name__ == '__main__':
    tokens = parse_document(
        'Hello there testing that this works that test seems to be working Hello')
    construct_reverse_index(tokens, '/wiki/Djokovic')
    # TODO: Need to pipe these into a file
    for key in sorted(reverse_index.keys()):
        print key, reverse_index[key]
