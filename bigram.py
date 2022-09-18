class Bigram():
    def __init__(self):
        self.root = {}
    
    def insert(self, previous, current):
        if previous not in self.root:
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

class node():
    def __init__(self):
        self.total = 0
        self.branches = {}

def preprocessing(training_set):
    file = 'a1/A1/A1_DATASET/train/{training_set}.txt'.format(training_set = training_set)
    processed_file = 'a1/A1/A1_DATASET/train/{training_set}_processed.txt'.format(training_set = training_set)
    with open(file, 'r') as f:
        lines = f.readlines()
    lines = ['<s> ' + line + '<stop>' for line in lines]
    with open(processed_file, 'w') as f:
        f.writelines(lines)

    return

def train(bigram):

    with open('a1/A1/A1_DATASET/train/truthful_processed.txt') as f:
        for line in f.readlines():
            words = line.split()
            for i in range(1, len(words)):
                bigram.insert(words[i-1], words[i])
    return

def main():
    preprocessing('deceptive')
    preprocessing('truthful')
    bigram = Bigram()
    train(bigram)
    print('Enter test words')
    test_words = input().split()
    if len(test_words) != 2:
        print('input 2 words')
    else:
        print('P(%s | %s):' % (test_words[0], test_words[1]), bigram.probability(test_words[0], test_words[1]))
    return

main()