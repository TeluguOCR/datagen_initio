#! /usr/bin/env python3
import sys
import os, re
import hashlib
from collections import defaultdict

def SplitFileName(filename):
    m = re.match('(.+?_.._.+?)(_.+_.+).tif', filename)
    return (m.group(1), m.group(2))

def chunk_reader(fobj, chunk_size=1024):
    """Generator that reads a file in chunks of bytes"""
    while True:
        chunk = fobj.read(chunk_size)
        if not chunk:
            return
        yield chunk

def DoIt(command):
    print(command)
    #os.system(command)

def check_for_duplicates(dir_name, hash=hashlib.sha1):
    print('Now doing directory : ', dir_name)
    hashes = {}
    top_bots = defaultdict(set)
    filenames = os.listdir(dir_name)
    for filename in filenames:
        full_path = os.path.join(dir_name, filename)
        hashobj = hash()
        for chunk in chunk_reader(open(full_path, 'rb')):
            hashobj.update(chunk)
        file_id = (hashobj.digest(), os.path.getsize(full_path))
        duplicate = hashes.get(file_id, None)
        if duplicate:
            # The file contents have been found - Just add top_bot info
            print("Duplicate found: {} and {}".format(full_path, duplicate))
            top_bots[duplicate].add(SplitFileName(full_path)[1])
            DoIt('rm '+ full_path)
        else:
            # The file contents have not been found, init a hash entry and a destination entry
            hashes[file_id] = full_path             
            top_bots[full_path].add(SplitFileName(full_path)[1])

    n, nretained = len(filenames), len(hashes)
    nremoved = n-nretained
    print('\t\tTotal {} = {} Removed ({:.1f}%) + {} Retained({:.1f}%)'.format(n, nremoved, nremoved*100./n, nretained, nretained*100./n))
    # Rename the keepees
    for filename in top_bots:
        if len(top_bots[filename]) == 1:
            continue
        new_fname = SplitFileName(filename)[0] + ''.join(tb for tb in top_bots[filename]) + '.tif'
        DoIt('mv '+ filename +  ' ' + new_fname)

input_dir = sys.argv[1]
if input_dir[-1] != '/':
    input_dir += '/'         
subdirs = os.listdir(input_dir)
for d in subdirs:
    check_for_duplicates(input_dir + d)
