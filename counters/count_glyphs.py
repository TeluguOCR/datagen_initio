#! /usr/bin/python3
# -*- coding: utf-8 -*-
import os
import pickle
import re
import sys
from collections import Counter

######################### Telugu Patterns
#([ఁ-ఔ])|(([క-హ]్)*[క-హ][ా-ౌ])|(([క-హ]్)*[క-హ](?![ా-్]))|(([క-హ]్)+(?=\s))

akshara_pattern = re.compile(r"""([ఁ-ఔౠౡ!(),\-.0-9=?'"౦-౯।॥])|	# Vowels
 (([క-హ]్)*[క-హ][ా-ౌ])|     # compounds
 (([క-హ]్)*[క-హ](?![ా-్]))|  # compounds in 'a'
 (([క-హ]్)+(?=\s))""", re.X)  # pollu
banti_pattern = re.compile(r'([క-హ])(?:(్[క-హ])*)([ా-్])?')
vattulu_pattern = re.compile(r'(్[క-హ])')


######################### Parse Arguments

try:
    input_file = sys.argv[1]
except IndexError:
    print("""Usage: {0} input_text_file [sortby]
    Program counts the frequency of each Banti Glyph and returns a list
    sorted by 0: letter 1: frequency
    """.format(sys.argv[0]))
    sys.exit()

try:
    sortby = int(sys.argv[2])
except IndexError:
    sortby = 0

######################### Process the text corpus
counts = Counter()
iline = 1

with open(input_file) as corpus:
    for line in corpus:
        if iline % 1000 == 0:
            print("Scanned {} Lines. Found {} unique and {} total glyphs."
                  "".format(iline, len(counts), sum(counts.values())))
        iline += 1

        for aksh_match in akshara_pattern.finditer(line):
            akshara = aksh_match.group()
            parts = banti_pattern.split(akshara)

            if len(parts) == 5:
                # For a perfect Match parts 0,4 should be empty
                if (parts[0], parts[4]) != ('', ''):
                    print("ERROR PARSING", akshara, parts[0], parts[4])

                # Gunintam is last part. Handle the not attaching ones
                if parts[3] is None:
                    gunintam = ''
                else:
                    gunintam = parts[3]

                if gunintam in ('ృ', 'ౄ', 'ౢ', 'ౣ'):  # ,'ై'
                    counts[gunintam] += 1
                    gunintam = ''  # if gunintam != 'ై' else 'ె'

                # Add the main akshara
                counts[parts[1] + gunintam] += 1

                # Add vottulu if present
                if parts[2] is not None:
                    for vattu in vattulu_pattern.split(parts[2]):
                        if vattu != '':
                            counts[vattu] += 1
            else:
                # Must be one of the vowels
                for part in parts:
                    if part != '':
                        counts[part] += 1

sort_counts = sorted(counts.items(), key=lambda x: x[sortby], reverse=sortby)


#########################
base = os.path.splitext(input_file)[0]
out_txt = base + '_glyph_counts.txt'
out_pkl = base + '_glyph_counts.pkl'

with open(out_txt, 'w') as f:
    for akshara, count in sort_counts:
        f.write("{0:7} - {1:7d}\n".format(akshara, count))

with open(out_pkl, 'wb') as f:
    pickle.dump(sort_counts, f)

print("Wrote output to \n{} \n{}".format(out_txt, out_pkl))