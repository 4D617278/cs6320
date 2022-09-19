def get_vocabulary(file):
    closed_vocabulary = {}
    with open(file, 'r') as f:
        for line in f.readlines():
            words = line.split()
            for i in words:
                if i not in closed_vocabulary:
                    closed_vocabulary[i] = True
    return closed_vocabulary

def mark_unknown(vocab, file):
    f_original = open(file, 'r')
    f_unknown = open('a1/A1/A1_DATASET/train/deceptive_unknown.txt', 'w')
    for line in f_original.readlines():
        words = line.split()
        for i in range(len(words)):
            if words[i] not in vocab:
                words[i] = '<unknown>'
        new_line = ' '.join(words) + '\n'
        f_unknown.writelines(new_line)
                


def main():
    truthful_file = 'a1/A1/A1_DATASET/train/truthful.txt'
    deceptive_file = 'a1/A1/A1_DATASET/train/deceptive.txt'
    closed_vocabulary = get_vocabulary(truthful_file)
    mark_unknown(closed_vocabulary, deceptive_file)

main()