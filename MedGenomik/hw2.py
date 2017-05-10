#- *- coding: UTF-8 -*-

import sys

inputNum = int(sys.argv[1])
print "The number for the SAM bit flag is ", inputNum
brinaryinputNum = bin(inputNum)
print "The brianry is  ", brinaryinputNum
explain = ["0x1    template having multiple segments in sequencing",
           "0x2    each segment properly aligned according to the aligner",
           "0x4    segment unmapped",
           "0x8    next segment in the template unmapped",
           "0x10   SEQ being reverse complemented",
           "0x20   SEQ of the next segment in the template being reversed 0x40 "
           "the first segment in the template",
           "0x80   the last segment in the template",
           "0x100  secondary alignment",
           "0x200  not passing quality controls",
           "0x400  PCR or optical duplicate",
           "0x800  suppleme"
           ]

# method 1
bits = 0
temp = inputNum
while(inputNum != 0):
	inputNum = inputNum >> 1
	bits += 1

inputNum = temp
flagBits = []
for i in range(bits):
	if(inputNum%2 == 0):
		flagBits.append(0)
		inputNum = inputNum >> 1
	else:
		flagBits.append(1)
		inputNum = inputNum >> 1
		print explain[i]

'''
i = 0
inputNum = temp
while (inputNum != 0):
	if (inputNum % 2 == 0):
		inputNum = inputNum >> 1
		i = i + 1
	else:
		inputNum = inputNum >> 1
		print explain[i]
		i = i + 1
'''

