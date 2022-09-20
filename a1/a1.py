#!/usr/bin/env python3

import sys

N = 2

if len(sys.argv) < 2:
	print(f'usage: {sys.argv[0]} <filename>')
	exit(1)

counts = [{} for i in range(N)]
probs = [{} for i in range(N)]

with open(sys.argv[1]) as f:
	for line in f.readlines():
		words = line.split(' ')

		for n in range(len(counts)):
			for i in range(len(words) - n):
				ngram = ' '.join(words[i:i + n + 1])
				if ngram in counts[n]:
					counts[n][ngram] += 1
				else:
					counts[n][ngram] = 1

# print(counts)

for i in range(len(counts)):
	for ngram in counts[i]:
		probs[i][ngram] = counts[i][ngram] / len(counts[i])

print(probs)
