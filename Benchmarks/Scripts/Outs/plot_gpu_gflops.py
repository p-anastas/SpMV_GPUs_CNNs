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
with open('cuSPARSE.out') as file:
	list0 = file.readlines()
with open('cuSP.out') as file:
	list1 = file.readlines()
with open('lightSpMV.err') as file:
	list2 = file.readlines()
with open('bhSPARSE.out') as file:
	list3 = file.readlines()

nm=["cuSP-scalar", "cuSP-vector", "lightSpMV-vector", "lightSpMV-warp", "bhSPARSE(CSR5)"]
files = len(list1)/20
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
	name.append(((list1[20*i+12].split()[2])[1:-1]).split('.')[0])
	nz 		= 	list1[20*i+12].split()[7]
	#print " (name=" + name + ", n=" + n + ", m=" + m + ", nz=" + nz + ")"
	
	res0.append(2*1000*float(nz)/((1024)**3*float(list0[i].split()[8])))
	res.append(list1[20*i+16].split()[5])
	res1.append(list1[20*i+15].split()[5])
	res2.append(float(list2[22*i+10].split()[1]))
	res3.append(float(list2[22*i+21].split()[1]))
	res4.append(list3[17*i+14].split()[12])

	if list1[20*i+17].split()[0]=="Refusing":
		res5.append("0.0")
	else:
		res5.append(list1[20*i+17].split()[5])

	if list1[20*i+18].split()[0]=="Refusing":
		res6.append("0.0")
	else:
		res6.append(list1[20*i+18].split()[5])

	if list1[20*i+19].split()[0]=="Refusing":
		res7.append("0.0")
	else:
		res7.append(list1[20*i+19].split()[5])

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
ax.set_ylabel('GFLOPS/s')
ax.set_xticks(ind + width / 2)
ax.set_xticklabels(name, rotation = (60))
#autolabel(rect)
ax.set_title( "Computation Benchmark" )
ax.legend(prop={'size':10},loc=2)
plt.savefig('Computation Benchmark.png', bbox_inches='tight')
plt.close()


	
