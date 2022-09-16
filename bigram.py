class Bigram():
    def __init__(self):
        self.root = {}
    
    def insert(self, previous, current):
        if previous not in self.root:
            self.root[previous] = node()
            self.root[previous].total += 1
        else:
            self.root[previous].total += 1
        if current not in self.root[previous]:
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
        branches = {}

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
    
    bigram = Bigram()
    with open('a1/A1/A1_DATASET/train/truthful.txt') as f:
        for line in f.readlines():
            words = line.split()

    return

preprocessing('deceptive')
preprocessing('truthful')

think = "<s> I booked two rooms four months in advance at the Talbott . We were placed on the top floor next to the elevators , which are used all night long . When speaking to the front desk , I was told that they were simply honoring my request for an upper floor , which I had requested for a better view . I am looking at a brick wall , and getting no sleep . He also told me that they had received complaints before from guests on the 16th floor , and were aware of the noise problem . Why then did they place us on this floor when the hotel is not totally booked ? A request for an upper floor does not constitute placing someone on the TOP floor and using that request to justify this . If you decide to stay here , request a room on a lower floor and away from the elevator ! I spoke at length when booking my two rooms about my preferences . This is simply poor treatment of a guest whom they believed would not complain . <stop>"
