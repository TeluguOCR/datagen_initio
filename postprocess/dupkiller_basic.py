#! /usr/bin/env python3

import sys
import os, re
import filecmp

def GetTopBottom(file_name):
    m = re.match('(.+)_(.+)_(.+)_(.+)_(.+).tif', file_name)
    return (m.group(4), m.group(5))

for dirpath, dirnames, filenames in os.walk(sys.argv[1]):
    print('Cleaning ... ', dirpath)
    for i in range(len(filenames)):
        i_file = os.path.join(dirpath, filenames[i])
        it, ib = GetTopBottom(i_file)
        for j in range(i+1, len(filenames)):
            j_file = os.path.join(dirpath, filenames[j])
            jt, jb = GetTopBottom(j_file)
            if it == jt and ib == jb and filecmp.cmp(i_file, j_file, shallow=False):
                #print(i_file, ' KILLED BY ' , j_file)
                os.system('rm '+i_file)
                break


