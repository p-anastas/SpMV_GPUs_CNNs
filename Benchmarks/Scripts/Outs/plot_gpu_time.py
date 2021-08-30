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

with open('cuSP-bench.out') as file:
	list1 = file.readlines()
with open('cuSPARSE-bench.out') as file:
	list2 = file.readlines()

nm=["CSR", "CSR-sor", "BSR(2)", "BSR(3)", "BSR(4)", "BSR(5)", "BSRW(2)", "BSRW(3)", "BSRW(4)", "BSRW(5)"]
k=0
while(1):
	while (list2[k].split()[-1]=='unsupported...terminating'):
		k+=2
	name=((list2[k].split()[1]).split('=')[1])[:-1]
	n = ((list2[k].split()[2]).split('=')[1])[:-1]
	m = ((list2[k].split()[3]).split('=')[1])[:-1]
	nz = ((list2[k].split()[4]).split('=')[1])[:-1]
	res2=[]
	ser= float((list2[k].split("t= ")[1]).split()[0])
	for x in range(1,11):
		res2.append(ser/(float((list2[k+x].split("t= ")[1]).split()[0])))
	k+=12
	fig, ax = plt.subplots(figsize=(16, 9),dpi=100)
	N = 10
	ind = np.arange(N)  # the x locations for the groups
	width = 0.5 # the width of the bars	
	rect2 = ax.bar(ind, res2, width, color='b',label='CUSPARSE')
	ax.set_ylabel('Speedup')
	ax.set_xlabel('Format')
	ax.set_xticks(ind + width / 2)
	ax.set_xticklabels(nm)
	#autolabel(rect2)
	ax.set_title('CUSPARCE '+ name + " (n=" + n + ", m=" + m + ", nz=" + nz + ")" )
	ax.legend(prop={'size':10},loc=2)
	plt.savefig('CuSPARCE_time_'+ name+'.png', bbox_inches='tight')
	plt.close()
	
