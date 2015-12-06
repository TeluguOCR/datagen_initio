#! /usr/bin/env python3
import os
import sys
from collections import Counter

########################## Process Arguments

try:
    img_dir = sys.argv[1]
except IndexError:
    print('Usage: ' + sys.argv[0] + ' <Directory>/ [banti_exe]\n'
          'Directory is location of the images to be fed to banti')
    sys.exit()

try:
    banti_exe = sys.argv[2] + ' '
except IndexError:
    banti_exe = 'bin/banti '

if img_dir[-1] != '/':
    img_dir += '/'
flags = ' 2 1 > '

########################### Process all the tif files with banti segmenter

file_list = sorted(os.listdir(img_dir))
for img_name in file_list:
    if img_name[-4:] != '.tif':
        print("Skipping non-TIFF file:", img_name)
        continue
    print("Feeding ", img_name)
    img_name = img_dir + img_name
    command = banti_exe + img_name + flags + img_name.replace('.tif', '.out')
    os.system(command)

################### Check to see if all the lines have equal words as expected

file_list = sorted(os.listdir(img_dir))
csv_file = open(img_dir + 'words_in_line.csv', 'w')
for out_fname in file_list:
    if out_fname[-4:] != '.out':
        continue

    for line in open(img_dir + out_fname):
        if line.find("Words_in_Line") == 0:
            line = line.replace("Words_in_Line", out_fname.replace('.out', ','))
            csv_file.write(line)
            counts = Counter([int(i) for i in line.rstrip().split(',')[2:-2]])
            if len(counts) != 1:
                print("Unequal number of 'words' per line in ", out_fname)
                print("Frequencies:", counts)
            break
    else:
        print("Did not find 'Words_in_Line' in ", out_fname)
csv_file.close()