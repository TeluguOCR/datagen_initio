#! /usr/bin/env python3
import sys, re, pickle
from math import log
from random import shuffle, seed

################### Arguments

try:
    input_file = sys.argv[1]
except IndexError:
    print('''Usage:{0} <glyph_count.pickle> [aksharas_per_line=30] [seed=84]
    Generates a nice training set with the log of glyph_count data
    given in the pickle file. aksharas_per_line is the aksharas per line.
    seed is random seed for shuffling'''.format(sys.argv[0]))
    sys.exit()

try:
    aksharas_per_line = int(sys.argv[2])
except IndexError:
    aksharas_per_line = 30

try:
    seed_at = int(sys.argv[3])
except IndexError:
    seed_at = 84

#################### Initializations

hallulu = []
hallulu2 = []  # The bad ones that better not be messed with
vattulu = []
achallulu = []
achallulu2 = []  # The bad ones again
ubhayalu = []
indeps = []
bad_consonants = 'ఖఘఙఛఝఞటఠఢథధపఫభమయషసహ'
bad_gunintams = 'ాుూొోౌ'  # All except ిీెే

with open(input_file, 'rb') as fp:
    counts = pickle.load(fp)

################# Read various letters

for akshara, count in counts:
    aksharas = list(akshara for i in range(1 + int(log(count, 2))))

    if re.match(r"""^[అ-ఔౠౡ!(),\-.0-9=?'"౦-౯।॥‌]$""", akshara):
        indeps += aksharas

    elif re.match(r'^[క-హ]$', akshara):
        if akshara[0] in bad_consonants:
            hallulu2 += aksharas
        else:
            hallulu += aksharas

    elif re.match(r'^్[క-హ]$', akshara):
        vattulu += aksharas

    elif re.match(r'^[ఁంఃృౄ]$', akshara):
        ubhayalu += aksharas

    elif re.match(r'^[క-హ][ా-ౌ]$', akshara):
        if akshara[1] == 'ై':
            indeps += aksharas
        elif akshara[0] in bad_consonants or akshara[1] in bad_gunintams:
            achallulu2 += aksharas
        else:
            achallulu += aksharas

    elif re.match(r'^[క-హ]్$', akshara):
        indeps += aksharas

    else:
        print("ERROR in recognizing ", akshara)

print("indeps ", len(indeps))
print("hallulu ", len(hallulu))
print("hallulu2 ", len(hallulu2))
print("ubhayalu ", len(ubhayalu))
print("achallulu ", len(achallulu))
print("achallulu2 ", len(achallulu2))
print("vattulu ", len(vattulu))

assert len(achallulu) >= len(vattulu)
assert len(hallulu) >= len(ubhayalu)

seed(seed_at)
shuffle(vattulu)
shuffle(ubhayalu)

print("Adding vattulu to acchallulu.")
for i in range(len(vattulu)):
    achallulu[i] = achallulu[i][0] + vattulu[i] + achallulu[i][1]

print("Adding ubhayalu to hallulu.")
for i in range(len(ubhayalu)):
    hallulu[i] += ubhayalu[i]

print("Combining and shuffling.")
text = indeps + hallulu + achallulu + hallulu2 + achallulu2
shuffle(text)

print("Adding space.")
spacing = '    '
data = ''
for t in text:
    data += t + spacing
data += 'ప్పు' + spacing + 'ఽ'

print("Splitting to appropriate {} chars per line.".format(aksharas_per_line))
find_cpl_letters = r'((?:.+?' + spacing + r'){' + str(aksharas_per_line) + r'})'
data = re.sub(find_cpl_letters, r'\1\n', data)
out_file = input_file.replace('.pkl',
                          '_{:d}_{:d}.txt'.format(aksharas_per_line, seed_at))

print("Writing output to file: ", out_file)
with open(out_file, 'w') as out_fp:
    out_fp.write(data)