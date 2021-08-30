import random
import matplotlib.pyplot as plt
import os
import copy
import sys


def is_non_zero_file(fpath):  
    return os.path.isfile(fpath) and os.path.getsize(fpath) > 0

if len (sys.argv) != 2:
	print ('Problem with input' )
else:
	src = str(sys.argv[1])
	for in_file in os.listdir(src):
		if is_non_zero_file(src + in_file)==False:
			if os.path.isfile(src + in_file)==True:
				print ( 'Found empty file: ' +  in_file)
				#print ( 'Executing: ' +  'mv ' + src + in_file + ' ' +  src + 'Removed/' + in_file )
				#os.system( 'mv ' + src + in_file + ' ' +  src + 'Removed/' + in_file)
			else:
				print ( 'Found a directory: ' +  in_file)
		else:
			status = os.stat(src+ in_file)
			if status.st_size > 1024*1024*501:
				print ( 'Found oversized file: ' +  in_file)
				print ( 'Executing: ' +  'mv ' + src + in_file + ' ' +  src + 'Oversized_500M/' + in_file )
				os.system( 'mv ' + src + in_file + ' ' +  src + 'Oversized_500M/' + in_file)






