import random
import matplotlib.pyplot as plt
import os
import copy
import sys
from scipy import sparse
from scipy import io

def is_non_zero_file(fpath):  
	return os.path.isfile(fpath) and os.path.getsize(fpath) > 0

def spyplot(x, str1):
	plt.spy(x, marker= '.', markersize=0.01)
	plt.axis('off')
	plt.savefig( str1 +'.png')
	plt.close()

def resize(A,mult1):
	if mult1==1:
		return sparse.coo_matrix((A.data, (A.row,A.col)), shape = A.shape)
	Brow = []
	Bcol = []
	Bdata = []
	for n in range(0, A.nnz):
		elem = A.data[n]
		for i in range(0,mult1):
			for j in range(0,mult1):
				Brow.append(mult*A.row[n] + i)
				Bcol.append(mult*A.col[n] + j)
				Bdata.append(elem)
	return sparse.coo_matrix((Bdata, (Brow,Bcol)), shape = ( A.shape[0]*mult, A.shape[1]*mult))

def mirror_copy4(A,i,j,k,l):
	Brow = []
	Bcol = []
	Bdata = []
	rows = A.shape[0]
	cols = A.shape[1]
	for n in range(0, A.nnz):
		elem = A.data[n]
		if i==0:		
			Brow.append(A.row[n])
			Bcol.append(A.col[n])
			Bdata.append(elem)
		else:
			Brow.append(A.row[n])
			Bcol.append(cols - A.col[n] -1)
			Bdata.append(elem)
		if j==0:		
			Brow.append(A.row[n])
			Bcol.append(cols + A.col[n])
			Bdata.append(elem)
		else:
			Brow.append(A.row[n])
			Bcol.append(2*cols - A.col[n] -1)
			Bdata.append(elem)
		if k==0:		
			Brow.append(rows + A.row[n])
			Bcol.append(A.col[n])
			Bdata.append(elem)
		else:
			Brow.append(rows + A.row[n])
			Bcol.append(cols - A.col[n]-1)
			Bdata.append(elem)
		if l==0:		
			Brow.append(rows + A.row[n])
			Bcol.append(cols + A.col[n])
			Bdata.append(elem)
		else:
			Brow.append(rows + A.row[n])
			Bcol.append(2*cols - A.col[n]-1)
			Bdata.append(elem)
	return sparse.coo_matrix((Bdata, (Brow,Bcol)), shape = ( A.shape[0]*2, A.shape[1]*2))


src = "/local/panastas/small_suite/"
dest = "/local/panastas/Augumented_small_suite/"
for in_file in sorted(os.listdir(src),reverse=True):
	if is_non_zero_file(src + in_file)==False:
		if os.path.isfile(src + in_file)==True:
			print ( 'Found empty file: ' +  in_file)
			continue
				#print ( 'Executing: ' +  'mv ' + src + in_file + ' ' +  src + 'Removed/' + in_file )
				#os.system( 'mv ' + src + in_file + ' ' +  src + 'Removed/' + in_file)
		else:
			print ( 'Found a directory: ' +  in_file)
			continue
	#Check 1M < file size < 500M
	status = os.stat(src+ in_file)
	if status.st_size > 1024*1024*125:
		print ( 'Found oversized file: ' +  in_file)
		print ( 'Executing: ' +  'mv ' + src + in_file + ' ' +  src + 'Oversized_500M/' + in_file )
		os.system( 'mv ' + src + in_file + ' ' +  src + 'Oversized_500M/' + in_file)
		continue
	elif status.st_size < 1024*2024:
		print ( 'Found very small file: ' +  in_file)
		print ( 'Executing: ' +  'mv ' + src + in_file + ' ' +  src + 'Small_2M/' + in_file )
		os.system( 'mv ' + src + in_file + ' ' +  src + 'Small_2M/' + in_file)
		continue


	## Open File/ Create Picture
	if in_file.endswith(".mtx"):
		A =  io.mmread(src+in_file)
		if sparse.issparse(A):
			density = 1.0*A.nnz/(A.shape[0]*A.shape[1])
			print (in_file+': nnz= ' + str( A.nnz ) +', density= '+ str( density ))
			if A.shape[0]!=A.shape[1]:
				print ('Not fair and square. Terminating')
				continue
			for i in range(0,2):
				for j in range(0,2):
					for k in range(0,2):
						for l in range(0,2):
							hush = i*8+j*4+k*2+l+1
							name = 'Augumented_'+ str(hush) + '_' + in_file
							if is_non_zero_file(dest+name):
								print ( "exists")
								continue
							B = mirror_copy4(A,i,j,k,l)
							density1 = 1.0*B.nnz/(B.shape[0]*B.shape[1])
							#print ( 'name=' + dest + name )
							io.mmwrite(dest+name, B, comment = 'An augumented matrix from ' + in_file)
							spyplot(B, dest + 'Pics/' + name )
							print ('Augumented ' + name +': nnz= ' + str( B.nnz ) + ', Out= '+ str(hush) +'/16 , density= '+ str( density1 ) )
			spyplot(A, dest + 'Pics/' + in_file )
			print ( 'Executing: ' +  'cp ' + src + in_file + ' ' +  dest +  in_file )
			os.system( 'cp ' + src + in_file + ' ' +  dest )
		else:
			print ( in_file+ ' is not sparse')
			print ( 'Executing: ' +  'mv ' + src + in_file + ' ' +  src + 'Removed/' + in_file )
			os.system( 'mv ' + src + in_file + ' ' +  src + 'Removed/' + in_file)

















