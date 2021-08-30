import os
import sys
from scipy import io

mypath = '/home/petyros/mount/Mine/training_suite/Matrices/'
writepath = '/home/petyros/mount/Mine/training_suite/'
files = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]



for filename in files:
	filepath = mypath + filename
	temp_info = io.mminfo(filepath)
	if temp_info[3] == 'coordinate':
		print (filename)
		temp_arr = io.mmread(filepath)
		io.mmwrite(writepath+filename, temp_arr, field = 'pattern')

