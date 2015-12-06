#! /usr/bin/env python3
import random, sys

SZ = int(sys.argv[1])
NOISE = int(sys.argv[2]) / 100
matrix = [0 for i in range(SZ) for j in range(SZ)]

def matxy(x, y):
	if x < SZ and y < SZ:
		return matrix[x+SZ*y]
	else:
		return 0

def matchxy(x, y):
	return '#' if matxy(x, y) else ' '

def printmat():
	print()
	for i in range(SZ):
		for j in range(SZ):
			print(matchxy(i, j), end='')
		print()
	print('                   -------------------------               ')

def neighbours(x, y):
	return ( matxy(x-1, y-1) + matxy(x, y-1) + matxy(x+1, y-1) +
			 matxy(x-1, y  ) + matxy(x, y)   + matxy(x+1, y)   +
			 matxy(x-1, y+1) + matxy(x, y+1) + matxy(x+1, y+1) )

def noisemat():
	for i in range(SZ):
		for j in range(SZ):
			score = neighbours(i, j)/9
			if random.random() < (score + NOISE):
				matrix[i+SZ*j] = 1

for i in range(int(sys.argv[3])):
	noisemat()
	printmat()



