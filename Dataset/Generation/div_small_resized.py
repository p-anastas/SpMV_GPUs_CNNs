import random
#import matplotlib.pyplot as plt
import os
import copy
import sys
from scipy import sparse
from scipy import io

def is_non_zero_file(fpath):  
	return os.path.isfile(fpath) and os.path.getsize(fpath) > 0

#def spyplot(x, str1):
	#plt.spy(x, marker= '.', markersize=0.01)
	#plt.axis('off')
	#plt.savefig( str1 +'.png')
	#plt.close()

def dg_dist(x, divz):
	z =  copy.deepcopy(x)
	for n in range(0, z.nnz-1):
		i = z.row[n]
		j = z.col[n]
		if i > j:
			zrow = i + (i-j)/divz
			if  zrow < z.shape[0]:
				z.row[n] = zrow
			else:
				z.row[n] = z.shape[0] - 1
		else:
			zcol = j + (j-i)/divz
			if zcol < z.shape[1]:
				z.col[n] = zcol
			else:
				z.col[n] = z.shape[1] - 1
	return z

def dg_dist_ng(x, divz):
	nz =  copy.deepcopy(x)
	for n in range(0, nz.nnz-1):
		i = nz.row[n]
		j = nz.col[n]
		if i > j:
			zrow = i - (i-j)/divz
			if  zrow >= 0 :
				nz.row[n] = zrow
			else:
				nz.row[n] = 0
		else:
			zcol = j - (j-i)/divz
			if zcol >= 0:
				nz.col[n] = zcol
			else:
				nz.col[n] = 0
	return nz

src = "/local/panastas/small_suite/"
dest = "/local/panastas/Div_small_suite/"
for in_file in os.listdir(src):
	if is_non_zero_file(src + in_file)==False:
		if os.path.isfile(src + in_file)==True:
			print ( 'Found empty file: ' +  in_file)
			continue
				#print ( 'Executing: ' +  'mv ' + src + in_file + ' ' +  src + 'Removed/' + in_file )
				#os.system( 'mv ' + src + in_file + ' ' +  src + 'Removed/' + in_file)
		else:
			print ( 'Found a directory: ' + in_file)
			continue
	#Check 2M < file size < 500M
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
			for divz in [2,3,4,6,8]:
				C = dg_dist(A, divz)
				#print ( 'in_file='+ dest + 'Divz_' +str(divz) + '_' + in_file )
				io.mmwrite(dest + 'Divz_' +str(divz) + '_' + in_file , C, comment = 'An artificial matrix from ' + in_file + 'with divz ' + str(divz))
				#spyplot(C, dest + 'Pics/' + 'Divz_' +str(divz) + '_' + in_file)
				density = 1.0*C.nnz/(C.shape[0]*C.shape[1])
				print ('Created ' + in_file +': nnz= ' + str( C.nnz ) + ', divz= '+ str(divz) +', density= '+ str( density ) )
				D = dg_dist_ng(A, divz)
				#print ( 'in_file=' +dest + 'Divz_-' + str(divz) + '_' + in_file )
				io.mmwrite(dest + 'Divz_-' + str(divz) + '_' + in_file , D, comment = 'An artificial matrix from ' + in_file+ 'with divz -' + str(divz))
				#spyplot(D, dest + 'Pics/' + 'Divz_-' +str(divz) + '_' +in_file)
				density1 = 1.0*D.nnz/(D.shape[0]*D.shape[1])
				print ('Created ' + in_file +': nnz= ' + str( D.nnz ) + ', divz= -'+ str(divz) +', density= '+ str( density ) )
			#spyplot(A, dest + 'Processed/Pics/' + in_file )
			print ( 'Executing: ' +  'mv ' + src + in_file + ' ' + src + 'Processed/' + in_file )
			os.system( 'mv ' + src + in_file + ' ' + src +  'Processed/' + in_file )
		else:
			print ( in_file+ ' is not sparse')
			print ( 'Executing: ' +  'mv ' + src + in_file + ' ' +  src + 'Removed/' + in_file )
			os.system( 'mv ' + src + in_file + ' ' +  src + 'Removed/' + in_file)
