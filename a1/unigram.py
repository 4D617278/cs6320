import numpy as np

class Unigram:
    def __init__(self):
        self.unigram = {}
        self.total = 0
        self.vocabulary = 0

    def insert(self, word):
        if word in self.unigram:
            self.unigram[word] += 1
            self.total += 1
        else:
            self.unigram[word] = 1
            self.total += 1
            self.vocabulary += 1
    
    def probability(self, word):
        probability = 0
        if word not in self.unigram:
            word = '<unknown>'
        probability = self.unigram[word] / self.total
        return probability

    def laplace(self, word):
        probability = 0
        if word not in self.unigram:
            word = '<unknown>'
        probability = (self.unigram[word]+1) / (self.total + self.vocabulary)
        return probability

    def add_k(self, k, word) :
        probability = 0
        if word not in self.unigram:
            word = '<unknown>'
        probability = (self.unigram[word]+k) / (self.total + (self.vocabulary * k))
        return probability

def train(unigram):

    with open('A1/A1_DATASET/train/truthful_processed.txt') as f:
        for line in f.readlines():
            words = line.split()
            for i in words:
                unigram.insert(i)
    
    with open('A1/A1_DATASET/train/deceptive_unknown_processed.txt') as f:
        for line in f.readlines():
            words = line.split()
            for i in words:
                unigram.insert(i)
    return

def main():
    unigram = Unigram()
    train(unigram)
    print('vocab:', unigram.vocabulary)
    print('Enter test word')
    test_word = input().split()
    if len(test_word) != 1:
        print('only input 1 word')
    else:
        test_word = test_word[0]
        print('P(%s):' % (test_word), unigram.probability(test_word))
        print('lapalce P(%s):' %(test_word), unigram.laplace(test_word))
        print('add_5 P(%s):' % (test_word), unigram.add_k(5, test_word))
    return
main()