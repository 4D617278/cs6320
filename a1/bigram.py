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
        if previous not in self.root:
            previous = '<unknown>'
        if next not in self.root[previous].branches:
            next = '<unknown>'
        probability = (self.root[previous].branches[next] + 1) / (self.root[previous].total + self.vocabulary)

        return probability

    def add_k(self, k, previous, next):
        probability = 0
        if previous not in self.root:
            previous = '<unknown>'
        if next not in self.root[previous].branches:
            next = '<unknown>'
        probability = (self.root[previous].branches[next] + k) / (self.root[previous].total + (self.vocabulary*k))
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
    lines = ['<s> ' + line for line in lines]
    with open(processed_file, 'w') as f:
        f.writelines(lines)

    return

def train(bigram):

    with open('A1/A1_DATASET/train/truthful_processed.txt') as f:
        for line in f.readlines():
            words = line.split()
            for i in range(1, len(words)):
                bigram.insert(words[i-1], words[i])

    with open('A1/A1_DATASET/train/deceptive_unknown_processed.txt') as f:
        for line in f.readlines():
            words = line.split()
            for i in range(1, len(words)):
                bigram.insert(words[i-1], words[i])
    return

def main():
    preprocessing('deceptive_unknown')
    preprocessing('truthful')
    bigram = Bigram()
    train(bigram)
    print('vocab:', bigram.vocabulary)
    print('Enter two words separated by spaces')
    test_words = input().split()
    if len(test_words) != 2:
        print('input 2 words')
    else:
        print('original P(%s|%s):' % (test_words[0], test_words[1]), bigram.probability(test_words[0], test_words[1]))
        print('laplace smoothing P(%s|%s):' % (test_words[0], test_words[1]), bigram.laplace(test_words[0], test_words[1]))
        print('add 5 smoothing P(%s|%s):' % (test_words[0], test_words[1]), bigram.add_k(5 ,test_words[0], test_words[1]))
    return

main()