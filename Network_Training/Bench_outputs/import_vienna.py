#	Input: 2 *.log files, containing normal and vienna benchmark results
#
#	Output: *.out1 file containing sum of benchmark results. Vienna failures accounted as 'Refusing ...'
#

import matplotlib.pyplot as plt
import numpy as np


with open('Div_small/dss_benchmark.log') as file:
	list0 = file.readlines()
with open('Div_small/vienna_dss_benchmark.log') as file:
	list1 = file.readlines()

outF = open("Div_small/dss_benchmark.out1", "w")
files = int(len(list0)/21)
print ("Files=" + str(files))
ctr = 0
ctrv= 0

for i in range(0,files):
	if list0[21*i].split()[1] != 'Benchmark':
		print ('Error, last array was ' + list0[21*i-21].split()[0])
		quit()

for i in range(0,files):
	for j in range(0,20):
		outF.write(list0[ctr])
		ctr = ctr + 1 
	if list1[ctrv+8].split()[2] != (list0[ctr-20].split()[0])[5:]:
		ctrv = ctrv +1
		if list1[ctrv] != 'ViennaCl\n':
			print ("error at " + list1[ctrv])
			break
		else :
			outF.write(list1[ctrv])

		ctrv = ctrv +1
		if list1[ctrv].split(':')[0] != 'Matrix':
			print ("error at " + list1[ctrv].split()[0])
			break
		else :
			outF.write(list1[ctrv])

		ctrv = ctrv +1
		if list1[ctrv].split()[2] != 'align1:':
			#print ("error at " + list1[ctrv].split()[2])
			outF.write("Refusing ...\n")
		else :
			outF.write(list1[ctrv])
			ctrv = ctrv +1

		if list1[ctrv].split()[2] != 'align4:':
			#print ("error at " + list1[ctrv].split()[2])
			outF.write("Refusing ...\n")
		else :
			outF.write(list1[ctrv])
			ctrv = ctrv +1

		if list1[ctrv].split()[2] != 'align8:':
			#print ("error at " + list1[ctrv].split()[2])
			outF.write("Refusing ...\n")
		else :
			outF.write(list1[ctrv])
			ctrv = ctrv +1

		if list1[ctrv].split()[1] != 'Hybrid:':
			#print ("error at " + list1[ctrv].split()[1])
			outF.write("Refusing ...\n")
		else :
			outF.write(list1[ctrv])
			ctrv = ctrv +1

		if list1[ctrv].split()[2] != 'Ell:':
			#print ("error at " + list1[ctrv].split()[2])
			outF.write("Refusing ...\n")
		else :
			outF.write(list1[ctrv])
			ctrv = ctrv +1


	else:
		ctrv = ctrv + 1
		for j in range(1,8):
			outF.write(list1[ctrv])
			ctrv = ctrv + 1
	outF.write(list0[ctr])
	ctr = ctr + 1
	ctrv = ctrv + 1
	
