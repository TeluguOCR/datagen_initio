#! /usr/bin/env python3
import os, sys
from fix_box_file import fix_box_file
from TeluguDiacriticMap import Map

try:
    prefix = sys.argv[1]
except IndexError:
    print('Usage: ' + sys.argv[0] + ''' <prefix for the images and text file>
        <prefix>.images are read one by one and box files are scanned using
        the text file <prefix>.txt and the script fix_box_file.py''')
    sys.exit()

if prefix[-1] != '.':
    prefix += '.'

img_dir = prefix + 'images/'
txt_file = prefix + 'txt'

dirtag = {'':img_dir+'good/', 'TOUCH':img_dir+'touch/'}
for i in dirtag:
    os.system('mkdir '+dirtag[i])

existings = set()
def ensure_dir(box):
    d = dirtag[box.error] + Map(box.text)
    if d not in existings:
        if not os.path.isdir(d):
            os.system('mkdir '+ d)
        existings.update(d)
    return d+'/'

def get_image_name(box, font_style):
    return '{}_{:03}{:03}_{}_{}.tif'.format(
        font_style, box.line, box.word,
        box.y - box.tl, 
        box.y + box.ht - box.bl)

file_list = [f for f in sorted(os.listdir(img_dir)) if f.endswith('.box')]

for box_file_name in file_list:        
    box_base_name = os.path.basename(box_file_name) 
    font_style = box_base_name[:-4]
    print(box_base_name)
    box_file_name = img_dir + box_file_name

    for box in fix_box_file(font_style, txt_file, box_file_name):
        img_name = ensure_dir(box) + get_image_name(box, font_style)
        command = "bin/six2tiff {} {} {} '{}'".format(
            box.wd, box.ht, img_name, box.pic)
        # print(img_name)
        os.system(command)