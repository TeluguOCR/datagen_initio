#!/usr/bin/env python3
import sys
from collections import Counter

if len(sys.argv) == 1:
    print('''Usage:{0} input_file
        Counts the number of occurences of each unicode character in 
        the given <input_file>'''.format(sys.argv[0]))
    sys.exit()

file_name = sys.argv[1]
count = Counter()
with open(file_name) as f:
    for line in f:
        count.update(line)

for char, k in sorted(count.items()):
    print(char, " ", k)