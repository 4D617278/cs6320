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

class Ngram():
    def __init__(self):
        self.root = {}
        self.total = 0
    
    def insert(self, previous, current):
        if previous not in self.root:
            self.total += 1
            self.root[previous] = Node()
            self.root[previous].total += 1
        else:
            self.root[previous].total += 1
        if current not in self.root[previous].branches:
            self.root[previous].branches[current] = 1
        else:
            self.root[previous].branches[current] += 1

    def prob(self, previous, next):
        prob = 0
        if previous not in self.root:
            return prob
        elif next not in self.root[previous].branches:
            return prob
        else:
            prob = self.root[previous].branches[next] / self.root[previous].total

        return prob

    def laplace(self, previous, next):
        return self.add_r(1, previous, next)

    def add_r(self, r, previous, next):
        if previous not in self.root:
            previous = '<unknown>'
        if next not in self.root[previous].branches:
            next = '<unknown>'
        prev_node = self.root[previous]
        return (prev_node.branches[next] + r) / (prev_node.total + r * self.total)

class Node():
    def __init__(self):
        self.total = 0
        self.branches = {}

def train(ngram, file):
    with open(file, 'r', errors='replace') as f:
        lines = f.read().splitlines()

    for line in lines:
        words = line.split(' ')
        for i in range(1, len(words)):
            ngram.insert(words[i - 1], words[i])

def perplexity(ngram, file):
    with open(file, 'r', errors='replace') as f:
        words = f.read().split(' ')

    for i in range(1, len(words)):
        ngram.insert(words[i - 1], words[i])

    sum = 0

    for i in range(1, len(words)):
        sum += log(ngram.prob(words[i - 1], words[i]))

    print(e ** (sum / len(words)))

def test(ngram, file):
    pass

START_INDEX = 1

def main():
    if len(argv) < START_INDEX + len(Class):
            args = ' '.join(c.name for c in Class)
            print(f'usage: {argv[0]} {args}')
            exit(1)

    files = [None] * len(Use)
    ngrams = [Ngram() for c in Class]

    for c in Class:
        path = argv[START_INDEX + c]

        with open(path) as f:
            files = f.read().splitlines()

        if len(files) < len(Use):
            print(f'bad file: {path}')
            exit(1)

        train(ngrams[c], files[Use.train])
        perplexity(ngrams[c], files[Use.validate])
        test(ngrams[c], files[Use.test])

if __name__ == '__main__':
        main()
