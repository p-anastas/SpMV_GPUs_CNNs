import matplotlib.pyplot as plt
import numpy as np
import math as ma
from matplotlib.ticker import ScalarFormatter

def f(x): # y axis
	y = x*peak_mem_gb
	if y<=peak_gflops:
		return y
	else:
		return peak_gflops

def f1(x): # y axis
	return x*peak_mem_gb


with open('cuSPARSE.out') as file:
	list0 = file.readlines()
with open('cuSP.out') as file:
	list1 = file.readlines()
with open('lightSpMV.err') as file:
	list2 = file.readlines()
with open('bhSPARSE.out') as file:
	list3 = file.readlines()

files = len(list1)/20

peak_gflops = 1681.0			# 1.681 TFlops/s from cuda profiler, 1.43 TFlops/s from Tesla k40m specs
peak_mem_gb = 288.384 * 0.767 	# 288.384 GB/s from cuda profiler, 288 GB/s from Tesla k40m specs, 76.7% sustained bandwith

x = np.arange(1/16.0, 128)
y= map(f,x)
y1= map(f1,x)


#x_axis = ["","1/8", "1/4", "1/2",	"1", 	"2", 	"4", 	"8", 	"16",	"32",	"64",	"128"]
#y_axis = ["","1/2", "1", 	"2",	"4",	"8",	"16",	"32",	"64",	"128",	"256",	"512",	"1024",	"2048"]



name=[]
for i in range(0,files):
	fig, ax = plt.subplots(figsize=(16, 9),dpi=300)
	plt.yscale('log', basey=2 )
	plt.xscale('log', basex=2)
	#ax.set_ylim(ymin=1/2.0, ymax = 512)
	ax.set_xlim(xmin=1/16.0, xmax = 128)

	for axis in [ax.yaxis]:
		axis.set_major_formatter(ScalarFormatter())

	ax.plot(x,y, color='r', )
	ax.plot(x,y1, dashes=[2, 2], color='k', alpha=0.7, label= "Memory bandwith * Operational intensity")
	plt.axhline(peak_gflops, 0, 1 ,dashes=[2, 2], color='b', alpha=0.7, label= "Device Max Double precision Flops/s")
	
	n = int(((list1[20*i+12].split()[5])[1:-1]).split(',')[0])
	m = int(((list1[20*i+12].split()[5])[1:-1]).split(',')[1])
	name.append(((list1[20*i+12].split()[2])[1:-1]).split('.')[0])
	nz 	= 	int(list1[20*i+12].split()[7])
	memory_footprint = 4*(n+1) + 4* nz + 8* nz 	# RowPtr[] + ColInd[] + Values[]
	memory_traffic = 8*n + 8*m 					# Reads from x[] and writes to y[] (assuming y is write only)?
	flops = 2 *nz								# 2 FP opperations/loop
	csr_op_in =  flops*1.0 / (memory_footprint + memory_traffic)
	print "Operational intensity= " + str(csr_op_in) +", Max GFlops/s= " + str(f(csr_op_in))
	plt.axvline(csr_op_in, 0, 1 ,dashes=[2, 2], color='g', alpha=0.7, label="Kernel Operational Intensity")
	ax.set_ylabel('GFLOPS/s')
	#ax.set_yticklabels(y_axis)
	#ax.set_xticklabels(x_axis)
	ax.set_title( "Roofline Analysis_" + name[i])
	ax.legend(prop={'size':10},loc=2)
	plt.savefig('./Roofline_graphs/Roofline_Analysis_' + name[i] + '.png', bbox_inches='tight')
	plt.close()


	
