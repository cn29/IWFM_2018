# parse result csv by Intel VTune
import csv
import pprint
import os
import operator
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

# np.set_printoptions(precision=2)
runtime = [565.5, 12806.8, 184.9, 543.1, 2825.3]
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

npercent = np.asarray(percent)
npercent_sum = np.sum(npercent, axis=0)
print(npercent_sum)
for idx in range(len(top_rountines)):
	if(top_rountines[idx].startswith('_')):
		top_rountines[idx]  = 'f'+top_rountines[idx];
	print(top_rountines[idx], end='\t')
	print(["{0:.1f}".format(perc) for perc in percent[idx]], end=' ')
	print(' ')

# plot
x = [0,1,2,3,4]
xlabels = ['SimC2V_CG\n%.1f%%'%npercent_sum[0], 'Butte\n%.1f%%'%npercent_sum[1], 'SimC2V_FG\n 1 years\n%.1f%%'%npercent_sum[2],
			'SimC2V_FG\n 3 years\n%.1f%%'%npercent_sum[3], 'SimC2V_FG\n 15 years\n%.1f%%'%npercent_sum[4]]
plt.figure()
#set x limits
plt.ylim((-1,25))
plt.xlim((-0.5, 4.5))
# set tick labels
plt.xticks([0, 1, 2, 3, 4], xlabels)

l0, = plt.plot(x, percent[0], label=top_rountines[0], marker='D')
l1, = plt.plot(x, percent[1], label=top_rountines[1], marker='D', color='red', linewidth=1.0, linestyle='--')
l2, = plt.plot(x, percent[2], label=top_rountines[2], marker='D', color='g', linewidth=1.0, linestyle='-')
l3, = plt.plot(x, percent[3], label=top_rountines[3], marker='D', color='c', linewidth=1.0, linestyle=':')
l4, = plt.plot(x, percent[4], label=top_rountines[4], marker='D', color='m', linewidth=1.0, linestyle='--')
l5, = plt.plot(x, percent[5], label=top_rountines[5], marker='D', color='y', linewidth=1.0, linestyle='--')
l6, = plt.plot(x, percent[6], label=top_rountines[6], marker='D', color='k', linewidth=1.0, linestyle='--')
l7, = plt.plot(x, percent[7], label=top_rountines[7], marker='D', color='b', linewidth=1.0, linestyle=':')
l8, = plt.plot(x, percent[8], label=top_rountines[8], marker='D', color='b', linewidth=1.0, linestyle='-')
l9, = plt.plot(x, percent[9], label=top_rountines[9], marker='D', color='c', linewidth=1.0, linestyle='-')


plt.legend(handles=[l0, l1, l2, l3, l4, l5, l6, l7, l8, l9], labels=top_rountines[0:10],  loc='best')
plt.show()