# parse result csv by Intel VTune
import csv
import pprint
import os
import numpy as np

# np.set_printoptions(precision=2)
runtime = [650, 15500, 670, 3000]
Dir = 'results_csv/'
filelist = os.listdir(Dir)
print(filelist)
table = [dict() for _ in range(len(filelist))]

for i in range(len(filelist)):
	with open(Dir+filelist[i], 'r') as f:
		readcsv = csv.reader(f, delimiter=',')
		for cnt, row in zip(range(15), readcsv):
			if cnt > 0:
				table[i][row[0]] = "{:.1f}".format(float(row[1])/runtime[i] * 100)

print(table[3])
pprint.pprint(table[1])

tableAll = dict()
for cnt, key in zip(range(6), table[0]):
	tableAll[key] = []
	for i in range(len(filelist)):
		if key in table[i]:
			tableAll[key].append(table[i][key])
		else:
			tableAll[key].append('NA')


pprint.pprint(tableAll)