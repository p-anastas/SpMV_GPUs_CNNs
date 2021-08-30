#	Input: 2 *.log files, containing normal and vienna benchmark results
#
#	Output: *.out1 file containing sum of benchmark results. Vienna failures accounted as 'Refusing ...'
#

import matplotlib.pyplot as plt
import numpy as np

with open('Div_small/dss_benchmark.out') as file:
	listtmp = file.readlines()
with open('Div_small/bsr_dss_benchmark.log') as file:
	list1 = file.readlines()

outFt = open("Div_small/dss_benchmark.outft", "w")
outF = open("Div_small/dss_benchmark.outf", "w")
files0 = int(len(listtmp)/32)
print ("Mixed Files=" + str(files0))
ctr = 0
ctrv= 0

for i in range (0,files0):
	if listtmp[32*i].split()[1] != 'Benchmark':
		print ('Error, last array was ' + listtmp[32*i-31].split()[0])
		quit()
	else:
		#if (listtmp[32*i]).find('Aug') >0:
		for j in range(0,32):
			outFt.write(listtmp[32*i+j])

outFt.close()
with open('Div_small/dss_benchmark.outft') as file:
	list0 = file.readlines()

files = int(len(list0)/32)
files1 = int(len(list1)/7)
print ("Files=" + str(files) + " vs " + str(files1))

for i in range (0,files):
	if list0[32*i].split()[1] != 'Benchmark':
		print ('Error, last array was ' + list0[32*i-31].split()[0])
		quit()

for i in range (0,files):
	if list1[7*i].split()[0] != list0[32*i].split()[0]:
		print ('Error, last arrays were ' + list1[7*i].split()[0] + ', ' + list0[32*i].split()[0])
		quit()

for i in range(0,files):
	for j in range(0,31):
		outF.write(list0[ctr])
		ctr = ctr + 1 
	if list1[ctrv+6].split()[2] != (list0[ctr-31].split()[0])[5:]:
		ctrv = ctrv +1
		if list1[ctrv] != 'cuSPARSE\n':
			print ("error at " + list1[ctrv])
			break
		else :
			outF.write(list1[ctrv])

		ctrv = ctrv +1
		if list1[ctrv].split()[1] != 'to':
			print ("error at " + list1[ctrv])
			break
		else :
			outF.write(list1[ctrv])

		ctrv = ctrv +1
		if list1[ctrv].split()[1] != 'version(dir=row,':
			print ("error at " + list1[ctrv])
			#outF.write("Refusing ...\n")
		else :
			outF.write(list1[ctrv])
			ctrv = ctrv +1

		if list1[ctrv].split()[1] != 'to':
			print ("error at " + list1[ctrv])
			#outF.write("Refusing ...\n")
		else :
			outF.write(list1[ctrv])
			ctrv = ctrv +1

		if list1[ctrv].split()[1] != 'version(dir=row,':
			print ("error at " + list1[ctrv])
			#outF.write("Refusing ...\n")
		else :
			outF.write(list1[ctrv])
			ctrv = ctrv +1
	else:
		ctrv = ctrv + 1
		for j in range(1,6):
			outF.write(list1[ctrv])
			ctrv = ctrv + 1
	outF.write(list0[ctr])
	ctr = ctr + 1
	ctrv = ctrv + 1
	
