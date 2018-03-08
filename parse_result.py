# parse result csv by Intel VTune
import csv
import pprint
import os
import operator
import numpy as np
import matplotlib.pyplot as plt

# np.set_printoptions(precision=2)
runtime = [650, 15500, 670, 3000]
Dir = 'results_csv/'
filelist = os.listdir(Dir)
print(filelist)
table = [dict() for _ in range(len(filelist))]

# renaming
# for i in range(len(filelist)):
# 	tmp = filelist[i].split('_')
# 	newname = tmp[0]+'_'+tmp[2][0:3]+'_'+tmp[1]+tmp[2][3:]
# 	os.rename(Dir+filelist[i], Dir+newname)

# filelist = os.listdir(Dir)
# print(filelist)filelist = os.listdir(Dir)

# remove file start with '.'
tmplist = []
for name in filelist:
	if not name.startswith('.'):
		tmplist.append(name)
filelist = tmplist

for i in range(len(filelist)):
	with open(Dir+filelist[i], 'r') as f:
		readcsv = csv.reader(f, delimiter=',')
		for cnt, row in zip(range(25), readcsv):
			if cnt > 0:
				#table[i][row[0]] = "{:.1f}".format(float(row[1])/runtime[i] * 100)
				table[i][row[0]] = float(row[1])/runtime[i] * 100

pprint.pprint(sorted(table[0].items(), key=operator.itemgetter(1), reverse=True))

# take intersection of top 6 subroutines from all experiments
N1 = 6
top_rountines = []
for i in range(len(filelist)):
	for idx, pair in zip(range(N1), sorted(table[i].items(), key=operator.itemgetter(1), reverse=True)):
		if pair[0] not in top_rountines:
			top_rountines.append(pair[0])

# print(' - ', '\n -  '.join(top_rountines))
print(' ', *top_rountines, sep='\n ')

# collect runtimes corresponding to top rountines in all experiments
percent = [[] for _ in range(len(top_rountines))]
for idx in range(len(top_rountines)):
	for i in range(len(filelist)):
		key = top_rountines[idx]
		if key in table[i]:
			percent[idx].append(table[i][key])
		else:
			percent[idx].append(0.0)

for idx in range(len(top_rountines)):
	print(top_rountines[idx], end='\t')
	print(["{0:.1f}".format(perc) for perc in percent[idx]], end=' ')
	print(' ')

# plot
xlabels = ['SimC2V_CG', 'Butte', 'SimC2V_FG 3 years', 'SimC2V_FG 15 years']	
plt.title(top_rountines[0])
plt.plot(percent[0])
plt.show()