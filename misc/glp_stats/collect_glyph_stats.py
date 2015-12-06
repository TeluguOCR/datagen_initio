#! /usr/bin/python
# -*- coding: utf-8 -*-

from PIL import Image
import sys, os, re

if len(sys.argv) < 2:
    print('Usage: ' + sys.argv[0] + ' <Directory>/ \n'
        'This Program finds the stats of images of each glyph class'
        'Directory is location of the directories containing image files for each glyph')
    sys.exit()

dirs_dir = sys.argv[1]
if dirs_dir[-1] != '/':
    dirs_dir += '/'

# Akshar_IT_4004018_-5_-28_-4_-27_-3_-26_-6_-29
# Font_Style_ID_T_B_T_B*
def SplitFileName(filename):
    m = re.match('(.+?)_(..)_.+?(_.+_.+).tif', filename)
    font = m.group(1)
    style = m.group(2)
    try:
        dtbs = map(int, m.group(3).split('_')[1:])
    except ValueError:
        print filename
        dtbs = []
    dtbpairs = [(dtbs[i], dtbs[i+1]) for i in range(0, len(dtbs), 2)]
    return font, style, dtbpairs

out_file = open('/tmp/' + dirs_dir[:-1].replace("/","_") + ".csv", 'w')
out_file.write("char font style wd ht xht normtop normbot normwd normht\n")

out_dir = '/tmp/avgs/' 
if not os.path.exists(out_dir): os.makedirs(out_dir)

NMXHT = 16 # This is the normalised height of the letter x (or ja in Telugu)
NMTOP = int(1.1 * NMXHT)
NMBOT = int(1.3 * NMXHT)
NMWID = 5 * NMXHT
NMHIT = NMTOP + NMXHT + NMBOT
idir = 0

for dirpath, dirnames, filenames in os.walk(dirs_dir):
    print idir, dirpath
    idir += 1
    big_im = Image.new("L", (NMWID, NMHIT), "white")
    big_im.load()
    char = os.path.basename(dirpath)
    nimgs  = 0
    for filename in filenames:
        # Sanity Checks and open
        if filename[-4:] != '.tif':
            print filename
            continue
        try:
            full_path = os.path.join(dirpath, filename)
        except NameError:
            print dirpath, filename
            raise
        # Open image and process
        im = Image.open(full_path)
        wd, ht = im.size
        font, style, dtbpairs = SplitFileName(filename)
        for dt, db in dtbpairs:
            xht   = dt + ht - db
            scalef = float(NMXHT)/xht
            normtop = int(scalef * dt)
            normbot = int(scalef * db) + NMXHT
            normwd  = int(scalef * wd)
            normht  = int(scalef * ht)

            # Write the stats to a file
            line     = " ".join(map(str, (char, font, style, wd, ht, xht, normtop, normbot, normwd, normht)))
            out_file.write(line+"\n")
            break

            # Scale and blend to get average
            #print nimgs
            try:
                nimgs = nimgs + 1
                im.load()
                im = im.convert('L')
                im = im.resize((normwd, normht))
                im2 = Image.new("L", (NMWID, NMHIT), "white")
                im2.load()
                im2.paste(im, (0, NMTOP + normtop))
                im2.load()
                big_im = Image.blend(big_im, im2, 1./nimgs)
            except:
                raise
                print char, nimgs,  big_im.size, im2.size
                continue
    try:
        big_im.save(out_dir + char + '.tif', 'TIFF')
    except:
        pass

out_file.close()


