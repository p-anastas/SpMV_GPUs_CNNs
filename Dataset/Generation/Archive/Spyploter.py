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

if len (sys.argv) != 3:
	print ('Problem with input' )
else:
	in_file = str(sys.argv[1])
	src = str(sys.argv[2])
	if in_file.endswith(".mtx"):
		try:
			A =  io.mmread(src+in_file)
		except:
			print ( 'Error with read, executing: ' +  'mv ' + src + in_file + ' ' +  src + 'Removed/' + in_file )
			os.system( 'mv ' + src + in_file + ' ' +  src + 'Removed/' + in_file)
