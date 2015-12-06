#! /usr/bin/env python3

import sys
import os, re
import filecmp

def GetTopBottom(file_name):
    m = re.match('(.+)_(.+)_(.+)_(.+)_(.+).tif', file_name)
    return (m.group(4), m.group(5))

for dirpath, dirnames, filenames in os.walk(sys.argv[1]):
    print('Cleaning ... ', dirpath, end=' ')
    # Read all files to memory
    dump = []
    for i in range(len(filenames)):
        i_file = os.path.join(dirpath, filenames[i])
        dump.append((i_file, GetTopBottom(i_file), open(i_file, 'rb').read()))
    n = len(dump)
    ndels = 0
    for i in range(n):
        for j in range(i+1, n):
            if dump[i][1] == dump[j][1] and dump[i][2] == dump[j][2]:
                #print(dump[i][0], ' KILLED BY ' , dump[j][0])
                os.system('rm '+dump[i][0])
                ndels += 1
                break
    if n: 
        print('Deleted {:5d}/{:5d} = {:2.2f}%'.format(ndels, n, ndels*100./n))
    del dump


