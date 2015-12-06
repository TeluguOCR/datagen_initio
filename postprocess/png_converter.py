#!/usr/bin/python
import sys, os
for dirpath, dirnames, filenames in os.walk(sys.argv[1]):
    print(dirpath)
    for filename in filenames:
        if filename[-4:] not in ('.TIF', '.tif'):
            print( "Skipping non tiff file", filename)
            continue
        file_path = os.path.join(dirpath, filename)
        os.system('convert {} {}'.format(file_path, file_path[:-4]+'.png'))
        os.system('rm '+file_path)

#tar -xf cbz.tar --wildcards --no-anchored '*.png'