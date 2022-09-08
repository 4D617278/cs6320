#!/usr/bin/env python3

import sys

if len(sys.argv) < 2:
	print(f'usage: {sys.argv[0]} <filename>')
	exit(1)

counts = {}

with open(sys.argv[1]) as f:
	for line in f.readlines():
		for word in line.split(' '):
			if word in counts:
				counts[word] += 1
			else:
				counts[word] = 1

print(counts)
