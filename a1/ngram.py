#!/usr/bin/env python3

from enum import IntEnum
from math import e, log
from os import listdir
from os.path import join
from sys import argv

class Class(IntEnum):
        truthful = 0
        deceptive = 1

class Use(IntEnum):
        train = 0
        validate = 1
        test = 2
        label = 3

class Ngram():
    def __init__(self):
        self.root = Node()
        self.total = 0 # vocabulary size

    def insert(self, words):
        cur = self.root

        for word in words:
            if word not in cur.branches:
                self.total += 1
                cur.branches[word] = Node()
            self.root.total += 1 # total number of words
            cur.branches[word].total += 1
            cur = cur.branches[word]

    def prob(self, words):
        if len(words) <= 0:
            return 0

        cur = self.root

        for word in words[:-1]:
            if word not in cur.branches:
                return 0
            cur = cur.branches[word]

        if words[-1] not in cur.branches:
            return 0
        return cur.branches[words[-1]].total / cur.total

    def laplace(self, words):
        return self.add_r(1, words)

    def add_r(self, r, words):
        if r <= 0 or self.root.total <= 0 or len(words) <= 0:
            return -1

        prob = r / (r * self.root.total)
        cur = self.root

        for word in words[:-1]:
            if word not in cur.branches:
                return prob
            cur = cur.branches[word]

        if words[-1] not in cur.branches:
            count = 0
        else:
            count = cur.branches[words[-1]].total

        return (count + r) / (cur.total + r * self.total)


class Node():
    def __init__(self):
        self.total = 0
        self.branches = {}

def train(ngram, lines, N):
    for line in lines:
        words = line.split(' ')
        for i in range(N, len(words) + 1):
            ngram.insert(words[i - N:i])

def perplexity(ngram, words, N, r):
    sum = 0

    for i in range(N, len(words) + 1):
        prob = ngram.add_r(r, words[i - N:i])
        if prob <= 0:
            return -1
        sum -= log(prob)

    return e ** (sum / len(words))

def test(ngrams, tests, labels, N, r):
    sum = 0
    for i in range(len(tests)):
        test_words = tests[i].split(' ')
        outputs = [perplexity(ngrams[c], test_words, N, r) for c in Class]
        #print(f'{labels[i]} {outputs} {min(outputs)}')
        sum += (int(labels[i]) == outputs.index(min(outputs)))

    print(f'Length: {N}, Accuracy: {sum / len(tests)}')
    print(f'Correct: {sum}')
     

START_INDEX = 2

N = 2 # unigram, bigram

def main():
    if len(argv) < START_INDEX + len(Class):
            args = ' '.join(c.name for c in Class)
            print(f'usage: {argv[0]} <smoothing> {args}')
            exit(1)

    try:
        smooth = float(argv[1])
    except ValueError:
        print('smoothing parameter must be nonnegative real')
        exit(1)

    if smooth < 0:
        print('smoothing parameter must be nonnegative real')
        exit(1)

    files = [None] * len(Use)
    ngrams = [[Ngram() for c in Class] for l in range(N)]
    sets = [None] * len(Use)

    for c in Class:
        path = argv[START_INDEX + c]

        with open(path) as f:
            files = f.read().splitlines()

        if len(files) < len(Use):
            print(f'bad file: {path}')
            exit(1)

        for u in Use:
            with open(files[u], 'r', errors='replace') as f:
                #if u == Use.validate:
                #    sets[u] = f.read().split(' ')
                #else:
                sets[u] = f.read().splitlines()

        for l in range(N):
            train(ngrams[l][c], sets[Use.train], l + 1)
            prplxty = perplexity(ngrams[l][c], sets[Use.validate], l + 1, smooth)
            print(f'Class: {c.name}, Length: {l + 1}, Perplexity: {prplxty}')

    for l in range(N):
        test(ngrams[l], sets[Use.test], sets[Use.label], l + 1, smooth)

if __name__ == '__main__':
        main()
