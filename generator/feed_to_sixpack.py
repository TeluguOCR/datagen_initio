#! /usr/bin/env python3
import os
import sys

try:
    img_dir = sys.argv[1]
except IndexError:
    print('Usage: {} <Directory>/'
          'All the "good" box files in the Directory will be six unpacked into '
          'TIFF files and saved as such'.format(sys.argv[0]))
    sys.exit()

if img_dir[-1] != '/':
    img_dir += '/'

six_pack_exe = 'bin/six_unpack '
file_list = sorted(os.listdir(img_dir))

for file_name in file_list:
    if file_name.endswith('good.box'):
        print("Feeding ", file_name)
        file_name = img_dir + file_name
        command = six_pack_exe + file_name
        os.system(command)