#	Input: *.out file in designated format
#
#	Output: Results/stats for target *.out file
#
import matplotlib.pyplot as plt
import numpy as np

def autolabel(rects):
    """
    Attach a text label above each bar displaying its height
    """
    for rect in rects:
        height = float(rect.get_height())
        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                '%.4f' % float(height),
                ha='center', va='bottom')
with open('Powerlaw_seq/powerlaw_sequence_benchmark.out') as file:
	list0 = file.readlines()


nm=["cuSPARSE-csr","cuSPARSE-hyb",  "cuSP-coo","cuSP-csr_scalar",  "cuSP-csr_vector", "cuSP-DIA", "cuSP-Ell", "cuSP-Hyb", "bhSPARSE(CSR5)", "lightSpMV-vector", "lightSpMV-warp", "vienna-align1", "vienna-align4", "vienna-align8", "vienna-Hyb", "vienna-Slicell" ]
nmctr=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
nmctr1=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
files = len(list0)/28
print "Files=" + str(files)
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
name=[]
for i in range(0,files):
	#n = ((list1[20*i+12].split()[5])[1:-1]).split(',')[0]
	#m = ((list1[20*i+12].split()[5])[1:-1]).split(',')[1]
	#name.append(((list1[28*i].split()[0])[1:-1]).split('.')[0])
	#nz 		= 	list1[20*i+12].split()[7]
	#print " (name=" + name[i] + ", n=" + n + ", m=" + m + ", nz=" + nz + ")"
	max1=[]
	res0.append(float(list0[28*i+3].split()[5]))
	res.append(float(list0[28*i+5].split()[5]))
	res1.append(float(list0[28*i+7].split()[4]))
	res2.append(float(list0[28*i+8].split()[4]))
	res3.append(float(list0[28*i+9].split()[4]))

	if list0[28*i+10].split()[0]=="Refusing":
		res4.append(0.0)
	else:
		res4.append(float(list0[28*i+10].split()[4]))

	if list0[28*i+11].split()[0]=="Refusing":
		res5.append(0.0)
	else:
		res5.append(float(list0[28*i+11].split()[4]))

	if list0[28*i+12].split()[0]=="Refusing":
		res6.append(0.0)
	else:
		res6.append(float(list0[28*i+12].split()[4]))

	res7.append(float(list0[28*i+16].split()[5]))
	res8.append(float(list0[28*i+18].split()[6]))
	res9.append(float(list0[28*i+19].split()[6]))


	if list0[28*i+22].split()[0]=="Refusing":
		res10.append(0.0)
	else:
		res10.append(float(list0[28*i+22].split()[7]))

	if list0[28*i+23].split()[0]=="Refusing":
		res11.append(0.0)
	else:
		res11.append(float(list0[28*i+23].split()[6]))

	if list0[28*i+24].split()[0]=="Refusing":
		res12.append(0.0)
	else:
		res12.append(float(list0[28*i+24].split()[6]))

	if list0[28*i+25].split()[0]=="Refusing":
		res13.append(0.0)
	else:
		res13.append(float(list0[28*i+25].split()[6]))

	if list0[28*i+26].split()[0]=="Refusing":
		res14.append(0.0)
	else:
		res14.append(float(list0[28*i+26].split()[7]))

	max1.append(float(res0[len(res0)-1]))
	max1.append(float(res[len(res)-1]))
	max1.append(float(res1[len(res1)-1]))
	max1.append(float(res2[len(res2)-1]))
	max1.append(float(res3[len(res3)-1]))
	max1.append(float(res4[len(res4)-1]))
	max1.append(float(res5[len(res5)-1]))
	max1.append(float(res6[len(res6)-1]))
	max1.append(float(res7[len(res7)-1]))
	max1.append(float(res8[len(res8)-1]))
	max1.append(float(res9[len(res9)-1]))
	max1.append(float(res10[len(res10)-1]))
	max1.append(float(res11[len(res11)-1]))
	max1.append(float(res12[len(res12)-1]))
	max1.append(float(res13[len(res13)-1]))
	max1.append(float(res14[len(res14)-1]))

	x = max(max1)
	#print x
	index = -1
	for j in range(0, len(max1)):
		if max1[j] == x:
			index = j
			max1[j] = 0.0
			break
	nmctr[index] = nmctr[index] + 1
	x = max(max1)
	#print x
	index = -1
	for j in range(0, len(max1)):
		if max1[j] == x:
			index = j
			max1[j] = 0.0
			break
	nmctr1[index] = nmctr1[index] + 1

#fig, ax = plt.subplots(figsize=(100, 9),dpi=300)
N = files
#ind = np.arange(N)  # the x locations for the groups
#width = 0.08 # the width of the bars	
#rect0 = ax.bar(ind, res0, width, color='r',label='cuSPARSE-csr')
#rect  = ax.bar(ind + 0.10, res, width, color='b',label='cuSP-csr_scalar')
#rect1 = ax.bar(ind + 0.20, res1, width, color='g',label='cuSP-csr_vector')
#rect5 = ax.bar(ind + 0.30, res5, width, color='k',label='cuSP-DIA')
#rect6 = ax.bar(ind + 0.40, res6, width, color='m',label='cuSP-Ell')
#rect7 = ax.bar(ind + 0.50, res7, width, color='c',label='cuSP-Hyb')
#rect2 = ax.bar(ind + 0.60, res2, width, color='y',label='lightSpMV-vector')
#rect3 = ax.bar(ind + 0.70, res3, width, color='darkorange',label='lightSpMV-warp')
#rect4 = ax.bar(ind + 0.80, res4, width, color='lime',label='bhSPARSE(CSR5)')
#plt.axhline(5.0,0,1 ,dashes=[2, 2], color='k', alpha=0.7)
#plt.axhline(10.0,0,1,dashes=[2, 2], color='k', alpha=0.7)
#plt.axhline(15.0,0,1,dashes=[2, 2], color='k', alpha=0.7 )
#plt.axhline(20.0,0,1,dashes=[2, 2], color='k', alpha=0.7 )
#plt.axhline(25.0,0,1,dashes=[2, 2], color='k', alpha=0.7 )
#plt.axhline(30.0,0,1,dashes=[2, 2], color='k', alpha=0.7 )
#ax.set_ylabel('GFLOPS/s')
#ax.set_xticks(ind + width / 2)
#ax.set_xticklabels(name, rotation = (60))
#autolabel(rect)
#ax.set_title( "Computation Benchmark" )
#ax.legend(prop={'size':10},loc=2)
#plt.savefig('Computation Benchmark.png', bbox_inches='tight')
#3plt.close()

for i in range(0, len(nmctr)):
	print  nm[i] + ": First = " + str(nmctr[i]) + " ( " + "%.2f" %(nmctr[i]*1.0/files*100) + "% ) / Second = " + str(nmctr1[i]) + " ( " + "%.2f" %(nmctr1[i]*1.0/files*100) + "% )"


	
