import matplotlib.pyplot as plt
import numpy as np

def autolabel(rects):
    """
    Attach a text label above each bar displaying its height
    """
    for rect in rects:
		height = int(rect.get_height())
		if height<>0.0:
			ax.text(rect.get_x() + rect.get_width()/2., 1.05*height, '%d' % int(height) ,ha='center', va='bottom')

			
with open('cuSP_conv.out') as file:
	list1 = file.readlines()
with open('bhSPARSE.out') as file:
	list2 = file.readlines()
with open('cuSPARSE.out') as file:
	list3 = file.readlines()
with open('cuSP.out') as file:
	list4 = file.readlines()

nm=["cuSP-scalar", "cuSP-vector", "lightSpMV-vector", "lightSpMV-warp", "bhSPARSE(CSR5)"]
files = len(list2)/17
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
name=[]
for i in range(0,files):
	#n = ((list1[20*i+12].split()[5])[1:-1]).split(',')[0]
	#m = ((list1[20*i+12].split()[5])[1:-1]).split(',')[1]
	name.append((list2[17*i+3])[14:-19])
	nz 		= 	list2[17*i+4].split()[6]
	#print " (name=" + name[i] +  ", nz=" + nz + ")"
	
	res.append("0.0")
	res0.append("0.0")
	res1.append("0.0")
	res2.append("0.0")
	res3.append("0.0")
	res4.append(float(list2[17*i+13].split()[3])/ (float(list3[i].split()[8]) - float(list2[17*i+14].split()[4])))
	if list1[18*i+14].split()[6]=="-1.00":
		res5.append("0.0")
	else:	
		res5.append(float(list1[18*i+14].split()[6]) /(float(list3[i].split()[8]) - float(list4[20*i+17].split()[5])))

	if list1[18*i+14].split()[8]=="-1.00":
		res6.append("0.0")
	else:
		res6.append(float(list1[18*i+14].split()[8]) /(float(list3[i].split()[8]) - float(list4[20*i+18].split()[5])))

	if list1[18*i+14].split()[10]=="-1.00":
		res7.append("0.0")
	else:
		res7.append(float(list1[18*i+14].split()[10]) /(float(list3[i].split()[8]) - float(list4[20*i+19].split()[5])))


fig, ax = plt.subplots(figsize=(100, 9),dpi=300)
N = files
ind = np.arange(N)  # the x locations for the groups
width = 0.08 # the width of the bars	
rect0 = ax.bar(ind, res0, width, color='r',label='cuSPARSE-csr')
rect  = ax.bar(ind + 0.10, res, width, color='b',label='cuSP-csr_scalar')
rect1 = ax.bar(ind + 0.20, res1, width, color='g',label='cuSP-csr_vector')
rect5 = ax.bar(ind + 0.30, res5, width, color='k',label='cuSP-DIA')
rect6 = ax.bar(ind + 0.40, res6, width, color='m',label='cuSP-Ell')
rect7 = ax.bar(ind + 0.50, res7, width, color='c',label='cuSP-Hyb')
rect2 = ax.bar(ind + 0.60, res2, width, color='y',label='lightSpMV-vector')
rect3 = ax.bar(ind + 0.70, res3, width, color='darkorange',label='lightSpMV-warp')
rect4 = ax.bar(ind + 0.80, res4, width, color='lime',label='bhSPARSE(CSR5)')
ax.set_ylabel('Preprocessing(preprocessing_time/(baseline_kernel_time-kernel_time))')
ax.set_xticks(ind + width / 2)
ax.set_xticklabels(name, rotation = (60))
autolabel(rect4)
autolabel(rect5)
autolabel(rect6)
autolabel(rect7)
ax.set_title( "Preprocessing time (from CSR)" )
ax.legend(prop={'size':10},loc=2)
plt.savefig('Preprocessing Benchmark.png', bbox_inches='tight')
plt.close()


	
