#	Input: *.out file in designated format
#
#	Data management: Keep top 5 implementations 
#
#	Output: File containing caffe compatible input format 
#	/path_to_pic_0/picture_type_0.png 0
#	/path_to_pic_1/picture_type_1.png 1	
#	...

import matplotlib.pyplot as plt
import numpy as np

in_file = 'training_suite_benchmark.out'
path = 'Training_suite/'
out_file = in_file.split('.')[0]

with open(path + in_file) as file:
	list0 = file.readlines()

outF = open(out_file + '.in', "w")

#nm=["cuSPARSE-csr","cuSPARSE-hyb",  "cuSP-coo","cuSP-csr_scalar",  "cuSP-csr_vector", "cuSP-DIA", "cuSP-Ell", "cuSP-Hyb", "bhSPARSE(CSR5)", "lightSpMV-vector", "lightSpMV-warp", "vienna-align1", "vienna-align4", "vienna-align8", "vienna-Hyb", "vienna-Slicell" ]
nm= ["cuSPARSE-csr","cuSPARSE-hyb",  "bhSPARSE(CSR5)",  "lightSpMV-warp", "vienna-align1" ]
nmctr=[0,0,0,0,0]#,0,0,0,0,0,0,0,0,0,0,0]
nmctr1=[0,0,0,0,0]#,0,0,0,0,0,0,0,0,0,0,0]
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
dire=[]
for i in range(0,files):
	#n = ((list1[20*i+12].split()[5])[1:-1]).split(',')[0]
	#m = ((list1[20*i+12].split()[5])[1:-1]).split(',')[1]
	name.append((list0[28*i].split()[0])[5:])
	dire.append(((list0[28*i+2].split()[0])[5:-5]).split(name[i])[0])
	#nz 		= 	list1[20*i+12].split()[7]
	#dire[i] = dire[i] + "Pics/"
	dire[i] = '/media/Shared/Drive/Diploma_thesis/Training_material/Neural_data/Bench_outputs/Div_small/Give_pics/'
	name[i] = name[i] + ".png"
	path = dire[i] + name[i]
	#print("Abs_path= " + path  )
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
	#max1.append(float(res1[len(res1)-1]))
	#max1.append(float(res2[len(res2)-1]))
	#max1.append(float(res3[len(res3)-1]))
	#max1.append(float(res4[len(res4)-1]))
	#max1.append(float(res5[len(res5)-1]))
	#max1.append(float(res6[len(res6)-1]))
	max1.append(float(res7[len(res7)-1]))
	#max1.append(float(res8[len(res8)-1]))
	max1.append(float(res9[len(res9)-1]))
	max1.append(float(res10[len(res10)-1]))
	#max1.append(float(res11[len(res11)-1]))
	#max1.append(float(res12[len(res12)-1]))
	#max1.append(float(res13[len(res13)-1]))
	#max1.append(float(res14[len(res14)-1]))

	x = max(max1)
	#print x
	index = -1
	for j in range(0, len(max1)):
		if max1[j] == x:
			index = j
			max1[j] = 0.0
			break
	#print (path + " " + str(index))
	outF.write(path + " " + str(index) + "\n")
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


for i in range(0, len(nmctr)):
	print  nm[i] + ": First = " + str(nmctr[i]) + " ( " + "%.2f" %(nmctr[i]*1.0/files*100) + "% ) / Second = " + str(nmctr1[i]) + " ( " + "%.2f" %(nmctr1[i]*1.0/files*100) + "% )"


	
