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
    reverse_index = defaultdict(list)
    counts = dict()
    for token in tokens:
        if token in counts:
            counts[token] += 1
        else:
            counts[token] = 1
    for key in counts:
        reverse_index[key].append((url, counts[key]))
    del counts
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
            pairs = ['%s:%d' % (pair[0], pair[1])
                     for pair in index[key]]
            pairs = [pair.encode('utf-8') for pair in pairs]
            key = key.encode('utf-8')
            f.write('%s--%s\n' % (key, ','.join(pairs)))


def construct_index(file_name):
    with open(file_name, 'r') as f:
        index = defaultdict(list)
        for line in f:
            try:
                line = line.strip()
                [key, values] = line.split('--')
                values = values.split(',')
                values = [(value.split(':')[0], int(value.split(':')[1]))
                          for value in values]
                index[key].extend(values)
            except:
                continue
        return index
    return None


if __name__ == '__main__':
    # This is for debugging purposes only
    tokens = parse_document(
        'Hello there, testing!Test.')
    index1 = construct_reverse_index(tokens, '/wiki/Djokovic')
    tokens = parse_document(
        'Hi there, I am still testing, will be done soon, hi!!!!!')
    index2 = construct_reverse_index(tokens, '/wiki/Nadal')
    merged_index = merge_reverse_indices(index1, index2)
    del index1, index2
    print_index(merged_index)
    dump_index(merged_index, 'index.txt')
    index = construct_index('index.txt')
    print_index(index)
