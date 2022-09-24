from math import e, log

class Bigram():
    def __init__(self):
        self.root = {}
        self.vocabulary = 0
    
    def insert(self, previous, current):
        if previous not in self.root:
            self.vocabulary += 1
            self.root[previous] = node()
            self.root[previous].total += 1
        else:
            self.root[previous].total += 1
        if current not in self.root[previous].branches:
            self.root[previous].branches[current] = 1
        else:
            self.root[previous].branches[current] += 1

    def probability(self, previous, next):
        probability = 0
        if previous not in self.root:
            return probability
        elif next not in self.root[previous].branches:
            return probability
        else:
            probability = self.root[previous].branches[next] / self.root[previous].total

        return probability

    def laplace(self, previous, next):
        probability = 0
        numerator = 0
        if previous not in self.root:
            previous = '<unknown>'
        if next not in self.root[previous].branches:
            numerator = 0
        else:
            numerator = self.root[previous].branches[next]
        probability = (numerator + 1) / (self.root[previous].total + self.vocabulary)

        return probability

    def add_k(self, k, previous, next):
        probability = 0
        if previous not in self.root:
            if '<unknown>' not in self.root:
                return k / (self.vocabulary*k)
            else:
                previous = '<unknown>'
        if next not in self.root[previous].branches:
            numerator = 0
        else:
            numerator = self.root[previous].branches[next]
        probability = (numerator + k) / (self.root[previous].total + (self.vocabulary*k))
        return probability

class node():
    def __init__(self):
        self.total = 0
        self.branches = {}

def preprocessing(training_set):
    file = 'A1/A1_DATASET/train/{training_set}.txt'.format(training_set = training_set)
    processed_file = 'A1/A1_DATASET/train/{training_set}_processed.txt'.format(training_set = training_set)
    with open(file, 'r') as f:
        lines = f.readlines()
    write = ''
    for line in lines:
        line = '<s> ' + line
        line = line.split()
        line.append('<stop>')
        line = ' '.join(line)
        write += line + '\n'
    with open(processed_file, 'w') as f:
        f.writelines(write)

    return

def train(bigram, file):

    with open(file) as f:
        for line in f.readlines():
            words = line.split()
            for i in range(1, len(words)):
                bigram.insert(words[i-1], words[i])
    return

def perplexity(bigram, words, k):
    '''
    sum = 0
    for i in range(1, len(words)):
        sum -= log(bigram.laplace(words[i-1], words[i]))
    print('laplace:', e ** (sum / len(words)))
    '''
    sum = 0
    for i in range(1, len(words)):
        sum -= log(bigram.add_k(k, words[i-1], words[i]))
    return e ** (sum / len(words))

def add_k_test(bigram_truthful, bigram_deceptive, k):
    correct = 0
    incorrect = 0

    # test on deceptive validation set
    deceptive_validation = open('A1/A1_DATASET/validation/deceptive_processed.txt')
    lines = deceptive_validation.readlines()
    for line in lines:

        truthful_ppl = perplexity(bigram_truthful, line.split(),k)
        deceptive_ppl = perplexity(bigram_deceptive, line.split(),k)
        # if deceptive ppl is lower, then the model is correct
        if deceptive_ppl < truthful_ppl:
            correct += 1
        else:
            incorrect += 1
    print('after testing on deceptive:')
    print('correct:', correct)
    print('incorrect:', incorrect)

    # test on truthful validation set
    truthful_validation = open('A1/A1_DATASET/validation/truthful_processed.txt')
    lines = truthful_validation.readlines()
    for line in lines:
        truthful_ppl = perplexity(bigram_truthful, line.split(), k)
        deceptive_ppl = perplexity(bigram_deceptive, line.split(), k)
        if truthful_ppl < deceptive_ppl:
            correct += 1
        else:
            incorrect += 1
    print('after testing on truthful:')
    print('correct:', correct)
    print('incorrect:', incorrect)

def test(bigram_truthful, bigram_deceptive, k):
    correct = 0
    incorrect = 0
    test_set = open('A1/A1_DATASET/test/test_processed.txt').readlines()
    test_labels = open('A1/A1_DATASET/test/test_labels.txt').readlines()
    for i in range(len(test_set)):
        truthful_ppl = perplexity(bigram_truthful, test_set[i].split(), k)
        deceptive_ppl = perplexity(bigram_deceptive, test_set[i].split(), k)
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
    preprocessing('truthful')
    preprocessing('deceptive')
    
    # bigrams for unknown implementation 1
    bigram_truthful1 = Bigram()
    bigram_deceptive1 = Bigram()

    # bigrams for unknown implementation 2
    bigram_truthful2 = Bigram()
    bigram_deceptive2 = Bigram()

    # unknown implementation 1 training
    train(bigram_truthful1, 'A1/A1_DATASET/train/truthful_processed.txt')
    train(bigram_deceptive1, 'A1/A1_DATASET/train/deceptive_unknown.txt')

    # unknown implementation 2 training
    train(bigram_truthful2, 'A1/A1_DATASET/train/truthful_unknown2.txt')
    train(bigram_deceptive2, 'A1/A1_DATASET/train/deceptive_unknown2.txt')
    
    print('test unknown implementation 1 on validation set:')
    add_k_test(bigram_truthful1, bigram_deceptive1, 0.00001)
    print('test unknown implementation 2 on validation set:')
    add_k_test(bigram_truthful1, bigram_deceptive2, 0.00005)
    
    print('final test on 1:')
    test(bigram_truthful1, bigram_deceptive1, 0.001)
    print('final test on 2:')
    test(bigram_truthful2, bigram_deceptive2, 0.000001)
    return

main()