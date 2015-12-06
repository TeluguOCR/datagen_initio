#!/usr/bin/python
import os, sys

testing = 0
def command(cmd):
    if testing:         print cmd
    elif cmd[0] != '_': os.system(cmd)

raise NotImplementedError, \
'''
Be sure what you are doing.
Keeps only one file of a given kind.
'''

idir = 0
for dirpath, dirnames, filenames in os.walk(sys.argv[1]):
    styles = set()
    glyph = os.path.basename(dirpath)
    idir += 1
    print idir, 'Processing images for ', glyph
    
    for filename in sorted(filenames):
        if filename[-4:] != '.tif':
            print( "Skipping non tiff file", filename)
            continue
        file_path = os.path.join(dirpath, filename)

        #Pothana_BL_4011002_-5_-1_2_1_1_0_-2_-3_3_2_-7_-2_-6_-1_0_4_-8_-4_0_-1_-2_2_-5_0.tif
        groups = filename.split('_')

        style = '_'.join(groups[:2])
        if style in styles: 
            command('rm '+file_path)
            continue
        styles.add(style)
        
        if len(groups) > 5:
            new_name = '_'.join(groups[:5])+'.tif'
            new_file_path = os.path.join(dirpath, new_name)
            command('mv {} {}'.format(file_path, new_file_path))
        else:
            command('__ '+file_path)
