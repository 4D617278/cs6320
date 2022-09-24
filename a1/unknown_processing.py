def get_vocabulary(file):
    closed_vocabulary = {}
    with open(file, 'r') as f:
        for line in f.readlines():
            words = line.split()
            for i in words:
                if i not in closed_vocabulary:
                    closed_vocabulary[i] = 1
                else:
                    closed_vocabulary[i] += 1
    return closed_vocabulary

def mark_unknown(vocab, file, set):
    f_original = open(file, 'r')
    f_unknown = open('A1/A1_DATASET/train/{set}_unknown.txt'.format(set=set), 'w')
    for line in f_original.readlines():
        words = line.split()
        for i in range(len(words)):
            if words[i] not in vocab:
                words[i] = '<unknown>'
        new_line = ' '.join(words) + '\n'
        f_unknown.writelines(new_line)

def main():
    truthful_file = 'A1/A1_DATASET/train/truthful_processed.txt'
    deceptive_file = 'A1/A1_DATASET/train/deceptive_processed.txt'
    truthful_closed_vocabulary = get_vocabulary(truthful_file)
    mark_unknown(truthful_closed_vocabulary, deceptive_file, 'deceptive')

main()