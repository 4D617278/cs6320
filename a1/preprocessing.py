def preprocessing(training_set):
    file = 'A1/A1_DATASET/test/{training_set}.txt'.format(training_set = training_set)
    processed_file = 'A1/A1_DATASET/test/{training_set}_processed.txt'.format(training_set = training_set)
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

def main():

    preprocessing('test')

    return

main()