class Unigram:
    def __init__(self):
        self.unigram = {}
        self.total = 0

    def insert(self, word):
        if word in self.unigram:
            self.unigram[word] += 1
            self.total += 1
        else:
            self.unigram[word] = 1
            self.total += 1
    
    def probability(self, word):
        if word not in self.unigram:
            return 0
        probability = self.unigram[word] / self.total
        return probability

def train(unigram):

    with open('a1/A1/A1_DATASET/train/truthful.txt') as f:
        for line in f.readlines():
            words = line.split()
            for i in words:
                unigram.insert(i)
    return

def main():
    unigram = Unigram()
    train(unigram)
    print('Enter test word')
    test_word = input().split()
    if len(test_word) != 1:
        print('only input 1 word')
    else:
        test_word = test_word[0]
        print('P(%s):' % test_word, unigram.probability(test_word))
main()