#! /usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
import cairo
import pango
import pangocairo
import sys
import os
from TeluguFontProperties import *

if len(sys.argv) < 2:
    print("""
Writes a given piece of text to an image files.
One image per font style.
The images will be located in <text_file>.images/*.tiff
Usage:
{0} <text_file>
 or
{0}  <(echo 'text')""".format(sys.argv[0]))
    sys.exit()

imagedir = sys.argv[1]
if imagedir.endswith('.txt'):
    imagedir = imagedir[:-4]
imagedir = imagedir + '.images/'
os.system('mkdir ' + imagedir)
print ("Output directory ", imagedir)

with open(sys.argv[1]) as fin:
    print("Opening ", sys.argv[1])
    text = fin.read().decode('utf8')

lines = text.split('\n')
n_lines = len(lines)
n_letters = max(len(line) for line in lines)
size_x = 30 * n_letters + 50  # TODO: Take into account # of spaces
size_y = 150 * n_lines + 25
print ("Lines: ", n_lines)
print ("Letters: ", n_letters)
print ("Size X: ", size_x)
print ("Size Y: ", size_y)

surf = cairo.ImageSurface(cairo.FORMAT_RGB24, size_x, size_y)
context = cairo.Context(surf)
pangocairo_context = pangocairo.CairoContext(context)
pangocairo_context.set_antialias(cairo.ANTIALIAS_SUBPIXEL)

layout = pangocairo_context.create_layout()
layout.set_text(text)


def filterfont(name):
    return False


style_ids = {'': '_NR', ' Bold': '_BL', ' Italic': '_IT', ' Bold Italic': '_BI'}

for fontname in sorted(FP_DICT):
    [sz, gho, rep, ppu, spc, abbr, hasbold] = FP_DICT[fontname]
    if filterfont(fontname):
        continue
    for style in style_ids:
        if not hasbold and style[:5] == ' Bold':
            print("No bold for ", abbr)
            continue
        fontname = fontname + ',' + style + ' ' + str(sz)
        font = pango.FontDescription(fontname)
        layout.set_font_description(font)
        layout.set_spacing(spc * 20480)
        context.rectangle(0, 0, size_x, size_y)
        context.set_source_rgb(1, 1, 1)
        context.fill()
        context.translate(50, 25)
        context.set_source_rgb(0, 0, 0)
        pangocairo_context.update_layout(layout)
        pangocairo_context.show_layout(layout)

        image_file_name = (imagedir + abbr + style_ids[style] + ".png").replace(
            " ", "_")
        print("Rendering ", abbr + style)
        with open(image_file_name, "wb") as image_file:
            surf.write_to_png(image_file)
        context.translate(-50, -25)

print("Converting PNGs to TIFs")
file_list = os.listdir(imagedir)
for png_name in sorted(file_list):
    if png_name[-4:] != '.png': continue
    png_name = imagedir + png_name
    os.system('bin/zealous ' + png_name)
    print ("Removing " + png_name)
    os.system('rm ' + png_name)
