import numpy as np
import random
import os
os.environ['GLOG_minloglevel'] = '2' # suprress Caffe verbose prints
import sys
sys.path.append("/home/users/athena/caffe/python")
import caffe
from caffe.proto import caffe_pb2
from caffe.io import blobproto_to_array
from PIL import Image

MODEL_FILE = '../caffe_train/Arch/lenet/lenet.prototxt' #'../caffe_train/Arch/Googlenet/deploy.prototxt'
#mu =   np.array([40.63,12.1037,4.67263]) # Binary -> np.array([238.168,230.447,216.007])    # Density + DDVT -> np.array([33.5282,10.0702,1.3628]) 
#print 'mean-subtracted values:', zip('BGR', mu)

def is_non_zero_file(fpath):  
	return os.path.isfile(fpath) and os.path.getsize(fpath) > 0


vpath_list = ['Augumented_block_arrays/', 'Div_small/', 'Powerlaw_cluster/', 'Powerlaw_seq/', 'Augumented_small/' , 'Validate_set/','Resized_small/', 'Training_suite/']# 
val_file_list = [ 'abs_benchmark.outf',  'div_small_resized_benchmark.outf', 'pc_benchmark.outf', 'psg_benchmark.outf', 'aass_benchmark.outf', 'ass_benchmark.outf','resized_small_benchmark.outf' , 'training_suite_benchmark.outf' ] # 

caffe.set_mode_gpu()
dirctr = 0
total_csr = 0 
total_csr5 = 0
for vpath in vpath_list:
	val_file = val_file_list[dirctr]
	dirctr = dirctr + 1

	with open(vpath + val_file) as file:
		list0 = file.readlines()
	
	files = len(list0)/37
	print ("Files=" + str(files))



	models = range(5000,10000,5000) # Nomean 120000, Mean 120000,420000  ['../Solverstates/Googlenet_iter_10000.caffemodel']
	for model in models: 
		#net = caffe.Classifier(MODEL_FILE, PRETRAINED, )
		#net = caffe.Net(MODEL_FILE, '../Solverstates/DDVT_dataset_Density/Lenet_iter_' + str(model) + '.caffemodel', caffe.TEST)
		#print ("successfully loaded Density_Googlenet iter " + str(model) )

		aver = [0,0,0,0,0,0,0,0,0]
		pred = [0,0,0,0,0,0]
		resol = 256
		r_pred=0
		r2_pred=0
		res0=[]
		res1=[]
		res2=[]
		res3=[]
		res4=[]
		res5=[]
		name=[]
		dire=[]
		nm= ["cuSPARSE-csr","cuSPARSE-hyb",  "bhSPARSE(CSR5)",  "lightSpMV-warp",  "merge-SpMV", "cuSPARSE-BSR(4)" ]
		nmctr=[0,0,0,0,0,0]
		aver = [0,0,0,0,0,0,0,0]
		processed = 0
		total_files = 0
		close_perf = 0

		for i in range(0,files):
			#n = ((list1[20*i+12].split()[5])[1:-1]).split(',')[0]
			#m = ((list1[20*i+12].split()[5])[1:-1]).split(',')[1]
			name.append((list0[37*i].split()[0])[5:])
			temp = ((list0[37*i+2].split()[0])[5:]).split('/')
			d = ''
			for x in range(0,len(temp)-1):
				d = d + temp[x] + '/'
			dire.append(d)
			#nz 		= 	list1[20*i+12].split()[7]
			dire[i] = dire[i] + "Density_pics/"
			#dire[i] = dire[i] + "Pics/Cropped_pics/"
			if name[i].find('Pw_') >= 0:
				if (name[i])[-6:-4] == '10':
					continue
				else:
					name[i] = name[i] + '_' + str(resol) +'.png'
					#name[i] = 'cr_' + name[i][:-4] + '.png'
			else:
				name[i] = name[i] + '_' + str(resol) +'.png'
				#name[i] = 'cr_' + name[i] + '.png'
			path1 = dire[i] + name[i]
			#print (path1)
			if is_non_zero_file(path1)==True:
				processed = processed + 1
			else: 
				continue
			#if (name[i])[0:3] == 'Aug':
			#	continue
			#print("Abs_path= " + path  )
		
			total_files = total_files + 1
			max1=[]
			res0.append(float(list0[37*i+3].split()[5]))
			res1.append(float(list0[37*i+5].split()[5]))
			res2.append(float(list0[37*i+16].split()[5]))
			res3.append(float(list0[37*i+19].split()[6]))
			res4.append(float(list0[37*i+30].split()[4]))	
			res5.append(float(list0[37*i+35].split()[8]))
			
		
			aver[0] = aver[0] + float(res0[len(res0)-1])
			aver[1] = aver[1] + float(res1[len(res1)-1])
			aver[2] = aver[2] + float(res2[len(res2)-1])
			aver[3] = aver[3] + float(res3[len(res3)-1])
			aver[4] = aver[4] + float(res4[len(res4)-1])
			aver[5] = aver[5] + float(res5[len(res5)-1])
		
			max1.append(float(res0[len(res0)-1]))
			max1.append(float(res1[len(res1)-1]))
			max1.append(float(res2[len(res2)-1]))
			max1.append(float(res3[len(res3)-1]))
			max1.append(float(res4[len(res4)-1]))
			max1.append(float(res5[len(res5)-1]))
	
			x = max(max1)
			marx= []
			prec = 0.00
			for j in range(0, len(max1)):
				if abs(max1[j]-x) <= prec*x: # Performance difference count
					marx.append(j)
			if len(marx) > 1 :
				#len_perf += len(marx)
				close_perf = close_perf + 1
			index = random.choice(marx)
			nmctr[index] = nmctr[index] + 1
			aver[6] = aver[6] + x
	
			# predict takes any number of images,
			# and formats them for the Caffe net automatically
			#transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
			#transformer.set_mean('data', mu)
			#transformer.set_transpose('data', (2,0,1))
			#transformer.set_channel_swap('data', (2,1,0))
			#transformer.set_raw_scale('data', 255)
			#net.blobs['data'].reshape(1,3,256,256)
			#im = caffe.io.load_image(path1)
			#print (name[i] + ": " + str(im.shape))
			#net.blobs['data'].data[...] = transformer.preprocess('data', im)
			#out = net.forward()
			#output_prob = out['prob'][0]
			#top_k = output_prob.argsort()[::-1][:6]
		
			#if top_k[0]==index or top_k[1] == index:
			#	r2_pred = r2_pred + 1
			#if top_k[0]==index:
			#	r_pred = r_pred + 1
		
			#pred[top_k[0]] = pred[top_k[0]] + 1
			#print ( "Prediction: " + str(top_k[0]) + " or " + str(top_k[1])  + " vs actual " + str(index) + " (" + str(r_pred) + "/" + str(total_files) + ")")	
			#aver[7] = aver[7] + max1[top_k[0]]
		total_csr5 = total_csr5 + aver[2]
		total_csr = total_csr + aver[0]
		#print (str(close_perf) + " implementations were closer than " + str(prec*100) + "%")
		print ("Average stats for " + str(total_files) + " arrays:	")
		#for i in range(0, len(nm)):
		#	print  (nm[i] + ": Average =  %.3f"  %(aver[i]/total_files) + " GFLOPs/s" )
		#for i in range(0, len(pred)):
		#	print  ('Predicted: ' + nm[i] + "= " + str(pred[i]) + "/" +str(total_files) )
		#	print  ('Actual: ' + nm[i] + "= " + str(nmctr[i]) + "/" +str(total_files) )
		#print  ("\nPrediction Accuracy =  %.2f"  %((1.0*r_pred/total_files)*100) + "%" )
		#print  ("Prediction Top_2 Accuracy =  %.2f"  %((1.0*r2_pred/total_files)*100) + "%" )
		#print  ("\nPredicted Average =  %.3f"  %(aver[7]/total_files) + " GFLOPs/s, Compared to CSR5: %.2f" %(aver[7]/total_files/(aver[2]/total_files)*100) )
		print  ("CSR5 Average =  %.3f"  %(aver[2]/total_files) + " GB/s, Compared to CSR: %.2f" %(aver[2]/aver[0]) )	
		print  ("Ideal Average =  %.3f"  %(aver[6]/total_files) + " GB/s, Compared to CSR: %.2f" %(aver[6]/aver[0]) )		
print  ("CSR5 Average Compared to CSR: %.2f" %(total_csr5/total_csr) )				
