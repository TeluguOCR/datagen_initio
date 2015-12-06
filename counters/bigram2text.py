#! /usr/bin/env python3

import re, sys, pickle
from random import randrange
from collections import defaultdict, Counter

if len(sys.argv) < 2:
    print("""Usage: {0} input_bigram_file [charsxlines]
Writes out a bunch of text based on the bigram strored in <input_bigram_file>
charsxlines is the amount of text to be written: defaults to 50x50
Output is written to <input_bigram_file>.txt
""".format(sys.argv[0]))
    sys.exit()

print("Loading the uni and bigram counts")
beg_line, end_line, unicount, bicount = pickle.load(open(sys.argv[1], "rb"))

if len(sys.argv) > 2:
    nchars = int(sys.argv[2].split('x')[0])
    nlines = int(sys.argv[2].split('x')[1])
else:
    nchars = 50
    nlines = 50

print("Of",nlines,"lines; now processing line:     ", end='')
char, sample_text = beg_line, ''
for i in range(nlines):
    print("\b\b\b\b{0:4d}".format(i+1), end="")
    for j in range(nchars):
        try:
            char = list(bicount[char].elements())[randrange(unicount[char])]
        except ValueError:
            print("ValueError for char : ", char)
            char = beg_line
        else:
            if char != end_line: 
                sample_text += char
            else:
                sample_text += " "
                char = beg_line
    sample_text += '\n'

with open(sys.argv[1]+'.txt', 'w')  as fsample:
    # Move dependent signs appearing at the beginning of a line to prev line
    fsample.write(re.sub(r"(?s)\n([ఁంః])", r"\1\n", sample_text))

print()