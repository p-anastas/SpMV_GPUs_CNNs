import sys
import os
import numpy as np
import time 

from PIL import Image
from scipy import sparse
from scipy import io


pic_arr = [256]
def is_non_zero_file(fpath):  
    return os.path.isfile(fpath) and os.path.getsize(fpath) > 0

def spyplot(x, str1):
	plt.spy(x, marker= '.', markersize=0.01)
	plt.axis('off')
	plt.savefig( str1 +'.png')
	plt.close()

def density_RGB(den, dtx,dty):
	temp = int(1.0 * den / ( dtx * dty) * (256**3))
	return ( temp / 256**2 , (temp % 256**2) / 256, (temp % 256**2) % 256)
	

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
				print ( 'Found a directory: ' +  in_file)
		else:
			if in_file.endswith(".mtx"):
				timer = time.clock()
				A =  io.mmread(src + in_file)
				timer = time.clock() - timer
				print ( "Input time: " + str(timer))
				dim_x = A.shape[0]
				dim_y = A.shape[1]
				if dim_x != dim_y:
					print( 'Uneven array' )
				datum_x = []
				datum_y = []
				last_x =[]
				last_y = []
				datum_density = []
				ctr = 0
				for pic_dim in pic_arr:
					datum_x.append( dim_x // (pic_dim - 1))
					datum_y.append( dim_y // (pic_dim - 1))
					last_x.append( dim_x - datum_x[ctr] * (pic_dim - 1))
					last_y.append( dim_y - datum_y[ctr] * (pic_dim - 1))
					print ( 'last_x = ' + str(last_x[ctr]) + ' last_y = ' + str(last_y[ctr]))
					print ( 'Array of shape ('  + str(dim_x) + ',' + str(dim_y) + ') with nnz= ' + str(len(A.row)) +  ' has datum (' + str(datum_x[ctr]) + ',' + str(datum_y[ctr]) + ')')
					datum_density.append (np.zeros((pic_dim,pic_dim),dtype=np.int8))
					ctr = ctr + 1
				timer = time.clock()
				for n in range(0,len(A.row)):
					for m in range(0,len(pic_arr)):
						dx = A.row[n] // datum_x[m]
						dy = A.col[n] // datum_y[m]
						if dx > (pic_dim - 1):
							dx = (pic_dim - 1)
						if dy > (pic_dim - 1):
							dy = (pic_dim - 1)
						(datum_density[m])[dx][dy] = (datum_density[m])[dx][dy] + 1
				timer = time.clock() - timer
				print ( "COO split time: " + str(timer))
				ctr = 0
				for pic_dim in pic_arr:
					pic = np.zeros((pic_dim,pic_dim, 3), dtype=np.uint8)
					for i in range(0,(pic_dim - 1)):
						for j in range(0,(pic_dim - 1)):
							(pic[i][j][0], pic[i][j][1], pic[i][j][2]) = density_RGB((datum_density[ctr])[i][j], datum_x[ctr], datum_y[ctr])
					if last_x != 0 and last_y !=0 :
						(pic[(pic_dim - 1)][(pic_dim - 1)][0], pic[(pic_dim - 1)][(pic_dim - 1)][1], pic[(pic_dim - 1)][(pic_dim - 1)][2]) = density_RGB((datum_density[ctr])[(pic_dim - 1)][(pic_dim - 1)], last_x[ctr], last_y[ctr])
					img2 = Image.fromarray(pic, 'RGB')
					img2.save(src + "Density_pics/"  + in_file + '_' + str(pic_dim) + '.png')
					ctr = ctr + 1
					print ( str(ctr) + ': processed image cr_' + in_file ) 
				ttimer = time.clock() - ttimer
				print( "Total time: " + str(ttimer))

