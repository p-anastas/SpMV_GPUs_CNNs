import random
import matplotlib.pyplot as plt
import os
import copy
import sys
from scipy import sparse
from scipy import io

def spyplot(x, str1):
	plt.spy(x, marker= '.', markersize=0.01)
	plt.axis('off')
	plt.savefig( str1 +'.png')
	plt.close()

def dg_dist(x, divz):
	z =  sparse.coo_matrix(x)
	for n in range(0, z.nnz-1):
		i = z.row[n]
		j = z.col[n]
		if i > j:
			zrow = i + (i-j)/divz
			if zrow < 0:
				z.row[n] = 0
			elif  zrow < z.shape[0]:
				z.row[n] = zrow
			else:
				z.row[n] = z.shape[0] - 1
		else:
			zcol = j + (j-i)/divz
			if zcol < 0:
				z.col[n] = 0
			elif zcol < z.shape[1]:
				z.col[n] = zcol
			else:
				z.col[n] = z.shape[1] - 1
	return z

def is_non_zero_file(fpath):  
    return os.path.isfile(fpath) and os.path.getsize(fpath) > 0

src = '/local/panastas/resized_small/' # '/home/users/panastas/Mine/training_suite/'
check = '/local/panastas/Div_resized_small/'
if len (sys.argv) != 3:
	print ('Problem with input' )
else:
	in_file = str(sys.argv[1])
	divz = int(sys.argv[2])
	if is_non_zero_file(check+ 'Divz_' +str(divz) + '_' + in_file)==False:
		status = os.stat(src+ in_file)
		if status.st_size > 1024*1024*500:
			print ( in_file + ' too large for div, terminating')
		else:
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
				else:
					dest =  '/local/panastas/Div_resized_small/' # '/home/users/panastas/Mine/python_pic/Outs/'
					name = in_file
					C = dg_dist(A, divz)
					io.mmwrite(dest + 'Divz_' +str(divz) + '_' + name , C, comment = 'An artificial matrix from ' + in_file + 'with divz ' + str(divz))
					spyplot(C, dest + 'Pics/' + 'Divz_' +str(divz) + '_' + name)
					density = 1.0*C.nnz/(C.shape[0]*C.shape[1])
					print ('Created ' + in_file +': nnz= ' + str( C.nnz ) + ', divz= '+ str(divz) +', density= '+ str( density ) )
			else:
				print ( in_file+ ' is not sparse')
	else:
		print ('Divz_' +str(divz) + '_' + in_file + ' generated already, checking for all')
		











