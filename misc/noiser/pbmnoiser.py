#! /usr/bin/env python3
import random, sys

class picture:
    def __init__(self, size, nois):
        self.w, self.h = size
        self.noise = nois
        self.data = [[0 for i in range(self.h)] for j in range(self.w)]

    def printpbm(self, fh, comment):
        fh.write('P1\n')
        fh.write('# '+comment+'\n')
        fh.write('{} {}\n'.format(self.w, self.h))
        for j in range(self.h):
            for i in range(self.w):
                fh.write(str(self.data[i][j]))
            fh.write('\n')

    def dxy(self, x, y):
        if x < self.w and y < self.h : 
            return self.data[x][y]
        else:
            return 0

    def neighbours(self, x, y):
        return ( self.dxy(x-1, y-1) + self.dxy(x, y-1) + self.dxy(x+1, y-1) +
                 self.dxy(x-1, y  ) + self.dxy(x, y)   + self.dxy(x+1, y)   +
                 self.dxy(x-1, y+1) + self.dxy(x, y+1) + self.dxy(x+1, y+1) )/9

    def noisemat(self, num_noises):
        for n in range(num_noises):
            for i in range(self.w):
                for j in range(self.h):
                    score = self.neighbours(i, j)
                    if random.random() < (score + self.noise)/(1+num_noises):
                        self.data[i][j] = 1

    def applymask(self, raw_data):
        for i in range(self.w):
            for j in range(self.h):
                self.data[i][j] = int(raw_data[j*self.w+i] and not self.data[i][j])

from papk_tiny import *

for i in range(10):
    noise_level = random.randrange(20) + 1
    pic = picture((width, height), noise_level/100)
    num_noises = random.randrange(1, 11, 2)
    pic.noisemat(num_noises)
    pic.applymask(my_pic_raw)
    comment = 'Noise level {}; Number of mutations {}'.format(noise_level, num_noises)
    name = '/tmp/{}_{}_{}.pbm'.format(i, noise_level, num_noises)
    fh = open(name, 'w')
    pic.printpbm(fh, comment)
    fh.close()
    
