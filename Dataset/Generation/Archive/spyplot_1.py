import random
import matplotlib.pyplot as plt
import os
import copy
import sys
from scipy import sparse
from scipy import io

def multgen(sz):
	mult = 2
	while sz*mult*mult <= 4000000:
		mult = mult+1
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

#out = open("generator.log",'w')
#for in_file in os.listdir("/local/panastas/small_suite_2.0/"):
if len (sys.argv) != 2:
	print ('Problem with input' )
else:
	in_file = str(sys.argv[1])
	if in_file.endswith(".mtx"):
		A =  io.mmread("/local/panastas/training_suite_2.0/"+in_file)
		if sparse.issparse(A):
			density = 1.0*A.nnz/(A.shape[0]*A.shape[1])
			print (in_file+': nnz= ' + str( A.nnz ) +', density= '+ str( density ))
			sz = A.nnz
			if sz < 312500:
				print ( in_file+ ' has too few nz' )
			elif sz <= 2000000:
				mult = multgen(sz)
				B = resize(A)	
				density1 = 1.0*B.nnz/(B.shape[0]*B.shape[1])
				if density1 != density:
					print( "Density not matching: " + str(density) + '!=' + str(density1) )
				print ('Resized ' + in_file +': nnz= ' + str( B.nnz ) + ', mult= '+ str(mult) +', density= '+ str( density ) )
				dest =  '/local/panastas/resized_suite/' # '/home/users/panastas/Mine/python_pic/Outs/'
				name = 'resized_'+ str(mult) + '_' + in_file
				#print ( 'name=' + dest + name )
				io.mmwrite(dest+name, B, comment = 'A resized matrix from ' + in_file)
				spyplot(B, dest + 'Pics/' + name )
				B =  sparse.coo_matrix(B)
			else:
				print ( in_file+ ' does not need resizing' )
				dest = '/local/panastas/normal_suite/' #'/home/users/panastas/Mine/python_pic/Tests/' 
				name = in_file
				B =  sparse.coo_matrix(A)
				spyplot(B, dest + 'Pics/' + name )
			for divz in [2,3,4,6,8]:
				C = dg_dist(B, divz)
				#print ( 'name='+ dest + 'Divz_' +str(divz) + '_' + name )
				io.mmwrite(dest + 'Divz_' +str(divz) + '_' + name , C, comment = 'An artificial matrix from ' + in_file + 'with divz ' + str(divz))
				spyplot(C, dest + 'Pics/' + 'Divz_' +str(divz) + '_' + name)
				density = 1.0*C.nnz/(C.shape[0]*C.shape[1])
				print ('Created ' + in_file +': nnz= ' + str( C.nnz ) + ', divz= '+ str(divz) +', density= '+ str( density ) )
				D = dg_dist_ng(B, divz)
				#print ( 'name=' +dest + 'Divz_-' + str(divz) + '_' + name )
				io.mmwrite(dest + 'Divz_-' + str(divz) + '_' + name , D, comment = 'An artificial matrix from ' + in_file+ 'with divz -' + str(divz))
				spyplot(D, dest + 'Pics/' + 'Divz_-' +str(divz) + '_' +name)
				density1 = 1.0*D.nnz/(D.shape[0]*D.shape[1])
				print ('Created ' + in_file +': nnz= ' + str( D.nnz ) + ', divz= -'+ str(divz) +', density= '+ str( density ) )
		else:
			print ( in_file+ ' is not sparse')











