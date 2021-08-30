#	Input: 2 files(.log, .out1), containing normal(with vienna) and merge benchmark results
#
#	Output: *.out file containing sum of benchmark results. Vienna failures accounted as 'Refusing ...'
#

import matplotlib.pyplot as plt
import numpy as np


with open('Div_small/dss_benchmark.out1') as file:
	list0 = file.readlines()
with open('Div_small/merge_dss_benchmark.log') as file:
	list1 = file.readlines()

outF = open("Div_small/dss_benchmark.out", "w")
files = int(len(list0)/28)
print ("Files=" + str(files))
ctr = 0
ctrv= 0

for i in range (0,files):
	if list0[28*i].split()[1] != 'Benchmark':
		print ('Error, last array was ' + list0[28*i-28].split()[0])
		quit()

for i in range (0,files):
	if list1[6*i].split()[0] != list0[28*i].split()[0]:
		print ('Error, last arrays were ' + list1[6*i].split()[0] + ', ' + list0[28*i].split()[0])
		quit()

for i in range(0,files):
	for j in range(0,27):
		outF.write(list0[ctr])
		ctr = ctr + 1 
	ctrv = ctrv + 1
	for j in range(1,5):
		outF.write(list1[ctrv])
		ctrv = ctrv + 1
	outF.write(list0[ctr])
	ctr = ctr + 1
	ctrv = ctrv + 1
	
