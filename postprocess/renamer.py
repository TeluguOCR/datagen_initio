#! /usr/bin/env python3
import sys, os, re

def ScanDir(d):
    print('In Dir', d)
    files = os.listdir(d)
    for f in files:
        m = re.match('(.+_.+_)(.+_.+_.+.tif)', f)
        if m == None:
            print("Could not match ", f)
            continue
        old_name = os.path.join(d, f)
        new_name = os.path.join(d, m.group(1)+sys.argv[2] + m.group(2))
        # print('mv ', old_name, ' ', new_name)
        os.system('mv ' + old_name + ' ' + new_name)

dirs = os.listdir(sys.argv[1])
for d in dirs:
    ScanDir(d)