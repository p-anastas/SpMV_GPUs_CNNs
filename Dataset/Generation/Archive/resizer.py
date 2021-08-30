import random
import matplotlib.pyplot as plt
import os
import copy
import sys
from scipy import sparse
from scipy import io

def multgen(sz):
	mult = 2
	while sz*mult*mult <= 2000000:
		mult = mult+1
	if mult > 4:
		mult = 4
	return mult

def spyplot(x, str1):
	plt.spy(x, marker= '.', markersize=0.01)
	plt.axis('off')
	plt.savefig( str1 +'.png')
	plt.close()

def resize(A):
	Brow = []
	Bcol = []
	Bdata = []
	for n in range(0, A.nnz):
		elem = A.data[n]
		for i in range(0,mult):
			for j in range(0,mult):
				Brow.append(mult*A.row[n] + i)
				Bcol.append(mult*A.col[n] + j)
				Bdata.append(elem)
	return sparse.coo_matrix((Bdata, (Brow,Bcol)), shape = ( A.shape[0]*mult, A.shape[1]*mult))

src = '/local/panastas/small_suite/' # '/home/users/panastas/Mine/training_suite/'
if len (sys.argv) != 2:
	print ('Problem with input' )
else:
	in_file = str(sys.argv[1])
	if in_file.endswith(".mtx"):
		A =  io.mmread(src+in_file)
		if sparse.issparse(A):
			density = 1.0*A.nnz/(A.shape[0]*A.shape[1])
			print (in_file+': nnz= ' + str( A.nnz ) +', density= '+ str( density ))
			sz = A.nnz
			if sz < 50000:
				print ( in_file+ ' has too few nz' )
				print ( 'Executing: ' +  'mv ' + src + in_file + ' ' +  src + 'Removed/' + in_file )
				os.system( 'mv ' + src + in_file + ' ' +  src + 'Removed/' + in_file)
				#print ( 'Executing: ' +  'rm -f ' + src + in_file )
				#os.system( 'rm -f ' + src + in_file)
			elif sz <= 2000000:
				mult = multgen(sz)
				B = resize(A)	
				density1 = 1.0*B.nnz/(B.shape[0]*B.shape[1])
				if density1 != density:
					print( "Density not matching: " + str(density) + '!=' + str(density1) )
				print ('Resized ' + in_file +': nnz= ' + str( B.nnz ) + ', mult= '+ str(mult) +', density= '+ str( density ) )
				dest =  '/local/panastas/resized_small/' # '/home/users/panastas/Mine/python_pic/Outs/'
				name = 'resized_'+ str(mult) + '_' + in_file
				#print ( 'name=' + dest + name )
				io.mmwrite(dest+name, B, comment = 'A resized matrix from ' + in_file)
				spyplot(B, dest + 'Pics/' + name )
				print ( 'Executing: ' +  'mv ' + src + in_file + ' ' +  src + 'Resized/' + in_file )
				os.system( 'mv ' + src + in_file + ' ' +  src + 'Resized/' + in_file)
			else:
				print ( in_file+ ' does not need resizing' )
		else:
			print ( in_file+ ' is not sparse')
			print ( 'Executing: ' +  'mv ' + src + in_file + ' ' +  src + 'Removed/' + in_file )
			os.system( 'mv ' + src + in_file + ' ' +  src + 'Removed/' + in_file)










