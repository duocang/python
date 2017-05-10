#encoding: utf-8
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import gzip
fname = '/Users/song/OneDrive/4/26040217/data/daughter_1.clean.fq.gz'
fq_info = []    # define a list to store read info
fq_seq = []     # define a list to store read sequence
gc_seq = []     # define a list tos tore GC content
fq_num = 1
#with gizp.open(fname, 'rb') as fq:
#for line in fq.readlines():
#line = line.rstrip()	# remove line break
with gzip.open(fname, 'rb') as input:
	for line in input:
		line = line.rstrip()
		if fq_num == 4:             # a forth line of each read block, it is score seq
			fq_seq.append(line)
			fq_num = 1
		elif fq_num == 2:           # a second line of each read block, it is GC seq
			gc_seq.append(line)
			fq_num = fq_num + 1
		else:
			fq_num = fq_num + 1

row = len(fq_seq)		            # this is the num of read, meaning how many lines it is read in
col = len(fq_seq[0])	            # this is the num of ATCG in each read/line

quality = []
temp = []

for j in range(len(fq_seq[0])):         # col 90
	for i in range(len(fq_seq)):		# row 20
		a = ord(fq_seq[i][j]) - 64
		temp.append(a)
	quality.append(temp)
	temp = []
#print quality[0]

print "problem 4"
gc = 0
gc_list = []
for i in range(row):
	for j in range(col):
		if(gc_seq[i][j] == "G"
		   or gc_seq[i][j] == "C"):
			gc = gc + 1
	gc_list.append(gc)
	gc = 0
print "G and C number in each read:"
print gc_list

plt.plot(gc_list, np.arange(0, row, 1) )
plt.title("GC distribution over all sequences ")
plt.annotate("small sample, data is not complete, so the shape is pretty bad",  xy=(1, 0))
plt.xlim(0, 90)
plt.show()


nnn = 0
nnn_list = []
for i in range(row):
	for j in range(col):
		if(gc_seq[i][j] != "A"
		   or gc_seq[i][j] != "T"
		   or gc_seq[i][j] != "C"
		   or gc_seq[i][j] != "G"):
			nnn = nnn + 1
	nnn_list.append(90 - nnn)
	nnn = 0
print "base N content: "
print nnn_list

plt.plot(np.arange(0, row, 1), nnn_list)
plt.ylim(-1, 100)
plt.annotate("N%", (90, 100))
plt.title("N content across all bases")
plt.show()


# ********pic of problem 3********
df = pd.DataFrame(np.transpose(quality))
df.boxplot()
plt.title("Quality scores across all bases(Illumina 1.5 encoding)")
plt.show()

# ********problem 5********
def print_kmers(seq, k):
	kmers = []
	n = len(seq)
	for i in range(0, n - k + 1):
		kmers.append(seq[i:i+k])
		print seq[i:i+k]

print_kmers(gc_seq[0], 4)

def count_kmers(seq, k):
	f = {}
	for x in range(len(seq)+1-k):
		kmer = seq[x:x+k]
		f[kmer] = f.get(kmer, 0) + 1
	return f

print count_kmers(gc_seq[0], 4)
