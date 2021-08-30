import matplotlib.pyplot as plt
import numpy as np
import random
import os
import sys

def autolabel(rects):
    """
    Attach a text label above each bar displaying its height
    """
    for rect in rects:
        height = float(rect.get_height())
        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                '%.4f' % float(height),
                ha='center', va='bottom')



def is_non_zero_file(fpath):  
	return os.path.isfile(fpath) and os.path.getsize(fpath) > 0


in_file = ['training_suite_benchmark.outf'] #  ,
path = [  './' ] # ,

resol = 256
nm=["cuSPARSE-csr","cuSPARSE-hyb",  "cuSP-coo","bhSPARSE(CSR5)", "lightSpMV-vector", "lightSpMV-warp", "vienna-align1",  "vienna-Slicell",  "merge-SpMV",  "BSR(4)" ]
#nm= ["cuSPARSE-csr","cuSPARSE-hyb",  "bhSPARSE(CSR5)",  "lightSpMV-warp",  "merge-SpMV", "cuSPARSE-BSR(4)" ]
#nmctr=[0,0,0,0,0,0]
closectr=[0,0,0,0,0,0]
nmctr=[0,0,0,0,0,0,0,0,0,0]
close_perf = 0
len_perf = 0
total_files = 0 
r_pred = 0
r2_pred = 0

for k in range(0,len(in_file)):
	#out_file = in_file[k].split('.')[0]
	#outF = open(out_file + '.in', "w")
	with open(path[k] + in_file[k]) as file:
		list0 = file.readlines()
	
	files = 1 #len(list0)/37

	print ("Files=" + str(files))
	res0=[]
	res=[]
	res1=[]
	res2=[]
	res3=[]
	res4=[]
	res5=[]
	res6=[]
	res7=[]
	res8=[]
	res9=[]
	res10=[]
	res14=[]
	res11=[]
	res12=[]
	res13=[]
	res15=[]
	res16=[]
	res17=[]
	name=[]
	dire=[]
	for i in range(0,files):
		#n = ((list1[20*i+12].split()[5])[1:-1]).split(',')[0]
		#m = ((list1[20*i+12].split()[5])[1:-1]).split(',')[1]
		name.append((list0[37*i].split()[0])[5:])
		temp = ((list0[37*i+2].split()[0])[5:]).split('/')

		total_files = total_files + 1
		max1=[]
		res0.append(float(list0[37*i+3].split()[5]))
		res.append(float(list0[37*i+5].split()[5]))
		res1.append(float(list0[37*i+7].split()[4]))
		res2.append(float(list0[37*i+8].split()[4]))
		res3.append(float(list0[37*i+9].split()[4]))
	
		if list0[37*i+10].split()[0]=="Refusing":
			res4.append(0.0)
		else:
			res4.append(float(list0[37*i+10].split()[4]))
	
		if list0[37*i+11].split()[0]=="Refusing":
			res5.append(0.0)
		else:
			res5.append(float(list0[37*i+11].split()[4]))
	
		if list0[37*i+12].split()[0]=="Refusing":
			res6.append(0.0)
		else:
			res6.append(float(list0[37*i+12].split()[4]))
	
		res7.append(float(list0[37*i+16].split()[5]))
		res8.append(float(list0[37*i+18].split()[6]))
		res9.append(float(list0[37*i+19].split()[6]))
	
	
		if list0[37*i+22].split()[0]=="Refusing":
			res10.append(0.0)
		else:
			res10.append(float(list0[37*i+22].split()[7]))
	
		if list0[37*i+23].split()[0]=="Refusing":
			res11.append(0.0)
		else:
			res11.append(float(list0[37*i+23].split()[6]))
	
		if list0[37*i+24].split()[0]=="Refusing":
			res12.append(0.0)
		else:
			res12.append(float(list0[37*i+24].split()[6]))
	
		if list0[37*i+25].split()[0]=="Refusing":
			res13.append(0.0)
		else:
			res13.append(float(list0[37*i+25].split()[6]))
	
		if list0[37*i+26].split()[0]=="Refusing":
			res14.append(0.0)
		else:
			res14.append(float(list0[37*i+26].split()[7]))
	
		res15.append(float(list0[37*i+30].split()[4]))	
		res16.append(float(list0[37*i+33].split()[8]))
		res17.append(float(list0[37*i+35].split()[8]))
fig, ax = plt.subplots(dpi=300) #figsize=(100, 9)
N = files
ind = np.arange(N)  # the x locations for the groups
width = 0.05 # the width of the bars	
#rect0 = ax.bar(ind, res0, width, color='r',label='cuSPARSE-csr')
rect0  = ax.bar(ind , res0, width, color='r',label='cuSPARSE-csr')
#autolabel(rect0)
rect  = ax.bar(ind + 0.10, res, width, color='g',label='cuSPARSE-hyb')
rect1 = ax.bar(ind + 0.20, res1, width, color='b',label='cuSP-coo')
#rect5 = ax.bar(ind + 0.15, res2, width, color='k',label='cuSP-csr_scalar')
#rect6 = ax.bar(ind + 0.20, res3, width, color='m',label='cuSP-csr_vector')
#rect7 = ax.bar(ind + 0.25, res4, width, color='g',label='cuSP-Hyb')
#rect0  = ax.bar(ind , res1, width, color='r',label='cuSP-coo')
#rect  = ax.bar(ind + 0.30, res5, width, color='b',label='cuSP-csr_scalar')
rect1 = ax.bar(ind + 0.30, res7, width, color='y',label='CSR5')
rect5 = ax.bar(ind + 0.40, res8, width, color='k',label='lightSpMV-vector')
rect6 = ax.bar(ind + 0.50, res9, width, color='m',label='lightSpMV-warp')
#rect7 = ax.bar(ind + 0.50, res9, width, color='g',label='vienna-align1')
rect0  = ax.bar(ind +0.6, res10, width, color='c',label='vienna-align1')
rect1 = ax.bar(ind + 0.70, res13, width, color='r',label='vienna-Slicell')
rect5 = ax.bar(ind + 0.80, res15, width, color='g',label='merge-SpMV')
#rect6 = ax.bar(ind + 0.85, res16, width, color='m',label='cuSP-Ell')
rect7 = ax.bar(ind + 0.90, res17, width, color='b',label='BSR(4)')
#rect2 = ax.bar(ind + 0.60, res2, width, color='y',label='lightSpMV-vector')
#rect3 = ax.bar(ind + 0.70, res3, width, color='darkorange',label='lightSpMV-warp')
#rect4 = ax.bar(ind + 0.80, res4, width, color='lime',label='bhSPARSE(CSR5)')
plt.axhline(5.0,0,1 ,dashes=[2, 2], color='k', alpha=0.7)
plt.axhline(10.0,0,1,dashes=[2, 2], color='k', alpha=0.7)
plt.axhline(15.0,0,1,dashes=[2, 2], color='k', alpha=0.7 )
plt.axhline(20.0,0,1,dashes=[2, 2], color='k', alpha=0.7 )
plt.axhline(25.0,0,1,dashes=[2, 2], color='k', alpha=0.7 )
plt.axhline(30.0,0,1,dashes=[2, 2], color='k', alpha=0.7 )
ax.set_ylabel('GFLOPS/s')
ax.set_xticks(ind + width / 2)
ax.set_xticklabels('')
#autolabel(rect1)
#autolabel(rect7)
ax.set_title( name[0] )
ax.legend(prop={'size':10},loc=2)
plt.savefig('CuSP_formats_performance1.png', bbox_inches='tight')
#3plt.close()

for i in range(0, len(nmctr)):
	print  nm[i] + ": First = " + str(nmctr[i]) + " ( " + str( nmctr[i]*1.0/files*100) + "% ) "

	
