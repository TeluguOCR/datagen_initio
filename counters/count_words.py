#! /usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys

try:
    corpus_file = sys.argv[1]
except IndexError:
    print("""Usage: {0} input_text_file [minimum_count]
    Program counts the frequency of each word and filters them 
    by the minimum_count if supplied and returns a list in ascending order
    """.format(sys.argv[0]))
    sys.exit()

try:
    cut_off = int(sys.argv[2])
except IndexError:
    cut_off = 0

#######################
counts = {}

with open(corpus_file) as dump:
    for line in dump:
        for word in line.split():
            try:
                counts[word] += 1
            except KeyError:
                counts[word] = 1


if cut_off:
    for k in list(counts.keys()):
        if counts[k] < cut_off:
            del counts[k]

#######################
base = os.path.splitext(corpus_file)[0]
out_txt = base + '_words_min{}.txt'.format(cut_off)

with open(out_txt, 'w') as f:
    for word in sorted(counts):
        f.write("{0:7} {1:7d}\n".format(word, counts[word]))

    f.write("#"*80 + "\n")
    sorted_counts = sorted(counts.items(), key=lambda x: (-x[1], x[0]))
    for word, count in sorted_counts:
        f.write("{} {}\n".format(count, word))

print("Wrote output to \n", out_txt)