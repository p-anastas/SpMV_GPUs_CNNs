#!/bin/bash 
import matplotlib
import copy
from matplotlib import pyplot as plt
import os
from scipy import sparse
from scipy import io
for file in os.listdir("/risky_store/athena/training_suite"):
	if file.endswith(".mtx"):
		A = io.mmread("/risky_store/athena/training_suite/" + file)
		density = 1.0*A.nnz/(A.shape[0]*A.shape[1])
		print (file+': nnz= ' + str( A.nnz ) + ', shape= ' + str( A.shape ) + ', density= '+ str( density ))
		markersize1=0.01
		plt.spy(A, marker= '.', markersize=markersize1)
		#plt.axis('off')
		plt.title('A: nnz= ' + str( A.nnz ) + ', size= ' + str( A.shape[0]*A.shape[1] ) + ', density= '+ str( density ))
		plt.savefig('./Tests/'+file+'_A_'+ str(markersize1)+' .png')
		plt.close()
		C = sparse.coo_matrix(A)
		for divz in [1,2,4,6,8]:
			B = copy.deepcopy(C)
			for n in range(0, B.nnz-1):
				i = B.row[n]
				j = B.col[n]
				if i > j:
					zrow = i + (i-j)/divz
					if  zrow < B.shape[0]:
						B.row[n] = zrow
					else:
						B.row[n] = B.shape[0] - 1
				else:
					zcol = j + (j-i)/divz
					if zcol < B.shape[1]:
						B.col[n] = zcol
					else:
						B.col[n] = B.shape[1] - 1
			plt.spy(B, marker= '.', markersize=markersize1)
			#plt.axis('off')
			plt.title('B: nnz= ' + str( B.nnz ) + ', size= ' + str( B.shape[0]*B.shape[1] ) + ', density= '+ str( density ))
			plt.savefig('./Tests/'+file+'_B_'+ str(divz)+' .png')
			plt.close()
		for divz in [8,6,4,2,1]:
			B = copy.deepcopy(C)
			for n in range(0, B.nnz-1):
				i = B.row[n]
				j = B.col[n]
				if i > j:
					zrow = i - (i-j)/divz
					if  zrow >= 0 :
						B.row[n] = zrow
					else:
						B.row[n] = 0
				else:
					zcol = j - (j-i)/divz
					if zcol >= 0:
						B.col[n] = zcol
					else:
						B.col[n] = 0
			plt.spy(B, marker= '.', markersize=markersize1)
			#plt.axis('off')
			plt.title('B: nnz= ' + str( B.nnz ) + ', size= ' + str( B.shape[0]*B.shape[1] ) + ', density= '+ str( density ))
			plt.savefig('./Tests/'+file+'_B_-'+ str(divz)+' .png')
			plt.close()
