#	Input: *.in file in designated format
#
#	Data management: Split data to training and testing sets at random
#
#	Output: 2 Files containing caffe compatible input format 
#	/path_to_pic_0/picture_type_0.png 0
#	/path_to_pic_1/picture_type_1.png 1	
#	...

import matplotlib.pyplot as plt
import numpy as np
import random

in_file = 'all_data_RGB.in'
path = ''
out_file1 = '../Training_data/train_' + in_file
out_file2 = '../Testing_data/test_' + in_file

with open(path + in_file) as file:
	list0 = file.readlines()

outF1 = open(out_file1 , "w")
outF2 = open(out_file2 , "w")

files = len(list0)

#Set testing data number
test_num = files/5

print ("Files= " + str(files) + ', Testing_data= ' + str(test_num))
test=[]
for i in range(0,test_num): 
	rand = random.randint(0,files-1)
	while rand in test:
		rand = random.randint(0,files-1)
	test.append(rand)
	outF2.write(list0[rand]) 

for i in range(0,files): 
	if i not in test:
		outF1.write(list0[i]) 

	
