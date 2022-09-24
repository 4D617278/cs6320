from math import e, log

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
            if '<unknown>' not in self.unigram:
                return probability
            else:
                word = '<unknown>'
        probability = self.unigram[word] / self.total
        return probability

    def add_k(self, k, word) :
        probability = 0
        if word not in self.unigram:
            if '<unknown>' not in self.unigram:
                return k / (self.total + self.vocabulary*k)
            else:
                word = '<unknown>'
        probability = (self.unigram[word]+k) / (self.total + (self.vocabulary * k))
        return probability
'''
    def laplace(self, word):
        probability = 0
        if word not in self.unigram:
            word = '<unknown>'
        probability = (self.unigram[word]+1) / (self.total + self.vocabulary)
        return probability
'''

def train(unigram, file):

    with open(file) as f:
        for line in f.readlines():
            words = line.split()
            for i in words:
                unigram.insert(i)
    return

def perplexity(unigram, words, k):
    sum = 0
    for i in range(1, len(words)):
        sum -= log(unigram.add_k(k, words[i]))
    return e ** (sum / len(words))

def validation_test(unigram_truthful, unigram_deceptive, k):
    correct = 0
    incorrect = 0

    # test on deceptive validation set
    deceptive_validation = open('A1/A1_DATASET/validation/deceptive.txt')
    lines = deceptive_validation.readlines()
    for line in lines:

        truthful_ppl = perplexity(unigram_truthful, line.split(),k)
        deceptive_ppl = perplexity(unigram_deceptive, line.split(),k)
        # if deceptive ppl is lower, then the model is correct
        if deceptive_ppl < truthful_ppl:
            correct += 1
        else:
            incorrect += 1
    print('after testing on deceptive:')
    print('correct:', correct)
    print('incorrect:', incorrect)

    # test on truthful validation set
    truthful_validation = open('A1/A1_DATASET/validation/truthful.txt')
    lines = truthful_validation.readlines()
    for line in lines:
        truthful_ppl = perplexity(unigram_truthful, line.split(), k)
        deceptive_ppl = perplexity(unigram_deceptive, line.split(), k)
        if truthful_ppl < deceptive_ppl:
            correct += 1
        else:
            incorrect += 1
    print('after testing on truthful:')
    print('correct:', correct)
    print('incorrect:', incorrect)

def test(unigram_truthful, unigram_deceptive, k):
    correct = 0
    incorrect = 0
    test_set = open('A1/A1_DATASET/test/test.txt').readlines()
    test_labels = open('A1/A1_DATASET/test/test_labels.txt').readlines()
    for i in range(len(test_set)):
        truthful_ppl = perplexity(unigram_truthful, test_set[i].split(), k)
        deceptive_ppl = perplexity(unigram_deceptive, test_set[i].split(), k)
        if test_labels[i].split()[0] == '0':
            if truthful_ppl <= deceptive_ppl:
                correct += 1
            else:
                incorrect += 1
        else:
            if deceptive_ppl <= truthful_ppl:
                correct += 1
            else:
                incorrect += 1
    print('correct:', correct)
    print('incorrect:', incorrect)

def main():
    # bigrams for unknown implementation
    unigram_truthful = Unigram()
    unigram_deceptive = Unigram()

    # training on unprocessed text
    train(unigram_truthful, 'A1/A1_DATASET/train/truthful.txt')
    train(unigram_deceptive, 'A1/A1_DATASET/train/deceptive.txt')

    print('test unigrams on validation set')
    validation_test(unigram_truthful, unigram_deceptive, 1)

    print('test on test set:')
    test(unigram_truthful, unigram_deceptive, 1)
    return
main()