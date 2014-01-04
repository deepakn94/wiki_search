from collections import defaultdict
from stemming.porter2 import stem
import nltk
from stopwords import stopwords
import string

exclude = set(string.punctuation)


def parse_document(text):
    tokens = nltk.word_tokenize(text)
    return [stem(token.lower()) for token in tokens if
            (token not in stopwords and token not in exclude)]


def construct_reverse_index(tokens, url):
    i = 0
    reverse_index = defaultdict(list)
    for token in tokens:
        reverse_index[token].append(url)
        i += 1
    return reverse_index


def merge_reverse_indices(index1, index2):
    merged_index = defaultdict(list)
    for key1 in index1:
        merged_index[key1].extend(index1[key1])
    for key2 in index2:
        merged_index[key2].extend(index2[key2])
    return merged_index


def print_index(index):
    for key in sorted(index.keys()):
        print key, index[key]


def dump_index(index, file_name):
    keys = sorted(index.keys())
    with open(file_name, 'w') as f:
        for key in keys:
            f.write('%s:%s\n' % (key, ','.join(index[key])))


def construct_index(file_name):
    with open(file_name, 'r') as f:
        index = defaultdict(list)
        for line in f:
            line = line.strip()
            [key, values] = line.split(':')
            values = values.split(',')
            index[key].extend(values)
        return index
    return None


if __name__ == '__main__':
    # This is for debugging purposes only
    tokens = parse_document(
        'Hello there, testing!Test.')
    index1 = construct_reverse_index(tokens, '/wiki/Djokovic')
    tokens = parse_document(
        'Hi there, I am still testing, will be done soon!!!!!')
    index2 = construct_reverse_index(tokens, '/wiki/Nadal')
    merged_index = merge_reverse_indices(index1, index2)
    del index1, index2
    print_index(merged_index)
    dump_index(merged_index, 'index.txt')
    index = construct_index('index.txt')
    print_index(index)
