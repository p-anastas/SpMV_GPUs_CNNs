import sys
import os
import numpy as np
import time 

from PIL import Image
from scipy import sparse
from scipy import io


pic_dim = 256
def is_non_zero_file(fpath):  
	return os.path.isfile(fpath) and os.path.getsize(fpath) > 0

def density_RGB(den, dtx,dty):
	temp1 = 1.0 * den / ( dtx * dty) * (256**3)
	if temp1 == float("inf"):
		print('Infinity again')
		return (-1,-1,-1)
	else:
		temp = int(temp1)
		return ( temp / 256**2 , (temp % 256**2) / 256, (temp % 256**2) % 256)

def datum_mapping(A):
	dim_x = A.shape[0]
	dim_y = A.shape[1]
	if dim_x != dim_y:
		print( 'Uneven array' )
		return []
	datum_x = dim_x // (pic_dim - 1)
	datum_y = dim_y // (pic_dim - 1)
	last_x = dim_x - datum_x * (pic_dim - 1)
	last_y = dim_y - datum_y * (pic_dim - 1)
	print ( 'last_x = ' + str(last_x) + ' last_y = ' + str(last_y))
	print ( 'Array of shape ('  + str(dim_x) + ',' + str(dim_y) + ') with nnz= ' + str(len(A.row)) +  ' has datum (' + str(datum_x) + ',' + str(datum_y) + ')')
	if datum_x==0 or datum_y==0:
		print( '0 datum, terminating...')
		return []
	datum_density = np.zeros((pic_dim,pic_dim),dtype=np.int8)
	timer = time.clock()
	for col,row in zip (A.col, A.row) :
		dx  = min(row // datum_x, pic_dim - 1)	
		dy  = min(col // datum_x, pic_dim - 1)					
		datum_density[dx][dy] = datum_density[dx][dy] + 1

	timer = time.clock() - timer
	print ( "COO split time: " + str(timer))
	pic = np.zeros((pic_dim,pic_dim, 3), dtype=np.uint8)
	for i in range(0,(pic_dim - 1)):
		for j in range(0,(pic_dim - 1)):
			(pic[i][j][0], pic[i][j][1], pic[i][j][2]) = density_RGB(datum_density[i][j], datum_x, datum_y)
	if last_x != 0 and last_y !=0 :
		(pic[(pic_dim - 1)][(pic_dim - 1)][0], pic[(pic_dim - 1)][(pic_dim - 1)][1], pic[(pic_dim - 1)][(pic_dim - 1)][2]) = density_RGB(datum_density[(pic_dim - 1)][(pic_dim - 1)], last_x, last_y)
	return pic

if len (sys.argv) != 2:
	print ('Problem with input' )
else:
	src = str(sys.argv[1])
	if os.path.isfile(src)==False:
		print ( 'Dir ' + src + ' found')
	#os.mkdir(src + 'Density_pics/')
	ctr = 0 
	for in_file in os.listdir(src):
		ttimer = time.clock()
		if is_non_zero_file(src + in_file)==False:
			if os.path.isfile(src + in_file)==True:
				print ( 'Found empty file: ' +  in_file)
				#print ( 'Executing: ' +  'mv ' + src + in_file + ' ' +  src + 'Removed/' + in_file )
				#os.system( 'mv ' + src + in_file + ' ' +  src + 'Removed/' + in_file)
			else:
				print ( 'Found a directory: ' +  src + in_file)
		else:
			if is_non_zero_file(src + "Density_pics/"  + in_file + '_' + str(pic_dim) + '.png'):
				continue
			print( 'Processing ' + in_file )
			if in_file.endswith(".mtx"):
				timer = time.clock()
				A =  io.mmread(src + in_file)
				if sparse.issparse(A)==False:
					print ('Matrix is not sparse')
					print ( 'Executing: ' +  'mv ' + src + in_file + ' ' +  src + 'Removed/' + in_file )
					os.system( 'mv ' + src + in_file + ' ' +  src + 'Removed/' + in_file)
					continue
				if (A.shape[0]!= A.shape[1]):
					print ('Dim missmatch:' + str(A.shape[0]) + ' != ' + str(A.shape[1]))
					print ( 'Executing: ' +  'mv ' + src + in_file + ' ' +  src + 'Removed/' + in_file )
					os.system( 'mv ' + src + in_file + ' ' +  src + 'Removed/' + in_file)
					continue
				timer = time.clock() - timer
				print ( "Input time: " + str(timer))
				pic = datum_mapping(A)
				if len(pic) == 0:
					print ( 'Executing: ' +  'mv ' + src + in_file + ' ' +  src + 'Removed/' + in_file )
					os.system( 'mv ' + src + in_file + ' ' +  src + 'Removed/' + in_file)
					continue
				img2 = Image.fromarray(pic, 'RGB')
				img2.save(src + "Density_pics/"  + in_file + '_' + str(pic_dim) + '.png')
				ctr = ctr + 1
				print ( str(ctr) + ': processed image cr_' + in_file ) 
				ttimer = time.clock() - ttimer
				print( "Total time: " + str(ttimer))

