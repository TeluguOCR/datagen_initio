#! /usr/bin/python3
# -*- coding: utf-8 -*-
import re
import sys
import os
from collections import Counter

try:
    corpus_file = sys.argv[1]
except IndexError:
    print("""Usage: {0} input_text_file [minimum_count]
    Program counts the frequency of each Telugu letter and filters them 
    by the minimum_count if supplied and returns a list in ascending order
    """.format(sys.argv[0]))
    sys.exit()

try:
    cut_off = int(sys.argv[2])
except IndexError:
    cut_off = 0

akshara_pattern = re.compile(
"([ఁ-ఔృౄౢౣ])|"                          # Duals, Vowels
"([0-9౦-౯])|"                        # Numbers
"([!(),\-.:;=?'\"।॥%&+<>])|"          # Punctuations
"( )|"                               # Space
"(([క-హ]్)*[క-హ][ా-ూె-ౌ])|"           # Compounds
"(([క-హ]్)*[క-హ](?![ా-ూె-్]))|"         # Compounds in 'a'
"(([క-హ]్)+(?=\s))")                 # Pollu
counts = Counter()

iline = 0
with open(corpus_file) as corpus:
    for line in corpus:
        for akshara_match in akshara_pattern.finditer(line):
            akshara = akshara_match.group()
            counts[akshara] += 1
        if not iline % 1000:
            print("Scanned {:,} lines. Found {:,} unique and {:,} total "
                  "aksharas.".format(iline, len(counts), sum(counts.values())))
        iline += 1

if cut_off:
    for k in list(counts.keys()):
        if counts[k] < cut_off:
            del counts[k]


#########################
base = os.path.splitext(corpus_file)[0]
out_txt = base + '_akshara_counts_min{}.txt'.format(cut_off)

with open(out_txt, 'w') as f:
    for akshara in sorted(counts):
        f.write("{0:7} {1:7d}\n".format(akshara, counts[akshara]))

    f.write("#"*80 + "\n")
    sorted_counts = sorted(counts.items(), key=lambda x: (-x[1], x[0]))
    for akshara, count in sorted_counts:
        f.write("{} {}\n".format(count, akshara))

print("Wrote output to \n", out_txt)