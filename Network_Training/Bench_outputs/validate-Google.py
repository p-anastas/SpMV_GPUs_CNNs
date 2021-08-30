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

deploy_list = [ '../caffe_train/Arch/Googlenet/deploy_372.prototxt','../caffe_train/Arch/Googlenet/deploy_372.prototxt',  '../caffe_train/Arch/Googlenet/deploy.prototxt', '../caffe_train/Arch/Googlenet/deploy.prototxt', '../caffe_train/Arch/Googlenet/deploy.prototxt']


def is_non_zero_file(fpath):  
	return os.path.isfile(fpath) and os.path.getsize(fpath) > 0


vpath_list = [ 'Augumented_block_arrays/', 'Div_small/', 'Powerlaw_cluster/', 'Powerlaw_seq/', 'Augumented_small/' ,'Validate_set/', 'Training_suite/']# 
val_file_list = [ 'abs_benchmark.outf',  'div_small_resized_benchmark.outf', 'pc_benchmark.outf', 'psg_benchmark.outf', 'aass_benchmark.outf',
'ass_benchmark.outf', 'training_suite_benchmark.outf' ] #  
nm= ["cuSPARSE-csr","cuSPARSE-hyb",  "bhSPARSE(CSR5)",  "lightSpMV-warp",  "merge-SpMV", "cuSPARSE-BSR(4)" ]
outstr = [' ','Sub-set & Size ','', '', '', '', '', '', '', '']
outstr1 = [' ','Sub-set & Size ','', '', '', '', '', '', '', '']
outstr2 = [' ','Format & Size ','', '', '', '', '', '', '', '']

for i in range(0,len(vpath_list)):
	outstr[i+2] = vpath_list[i] 
	outstr1[i+2] = vpath_list[i] 

for i in range(0,len(nm)):
	outstr2[i+2] = nm[i] 

caffe.set_mode_gpu()
models = [  '../Solverstates/Small_dataset_Binary/Binary_Googlenet_iter_70000.caffemodel' , '../Solverstates/Total_dataset_binary/Binary_Googlenet_iter_80000.caffemodel' , '../Solverstates/DDVT_dataset_Density/Googlenet_iter_420000.caffemodel', '../Solverstates/Small_dataset_Density/Density_Googlenet_iter_100000.caffemodel', '../Solverstates/Total_dataset_binary/Density_Googlenet_iter_80000.caffemodel' ] # Nomean 120000, Mean 120000,420000  ['../Solverstates/Googlenet_iter_10000.caffemodel']
model_type = [0,0,1,1,1]
#mulist =   [np.array([0,0,0]), np.array([34.4794,10.3774,1.44179]), np.array([40.1584,12.0457,4.6718])]
mulist = [  np.array([238.238,230.556,216.178]),  np.array([241.473,235.017,223.23]), np.array([34.4794,10.3774,1.44179]), np.array([40.1584,12.0457,4.6718]), np.array([30.1884,10.4965,3.14379]) ]
print 'mean-subtracted values:', zip('BGR', mulist)
for model,mtype,mu, deploy_f in zip(models, model_type,mulist, deploy_list) : 
	#net = caffe.Classifier(MODEL_FILE, PRETRAINED, )
	net = caffe.Net(deploy_f,model, caffe.TEST)
	print ("successfully loaded " + str(model) )
	dirctr = 0
	Acc = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
	Acc_top2 = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
	t_pred = [0,0,0,0,0,0]
	rec_pred =  [0,0,0,0,0,0]
	t_nmctr=[0,0,0,0,0,0]
	t_total = 0
	for vpath in vpath_list:
		val_file = val_file_list[dirctr]

		with open(vpath + val_file) as file:
			list0 = file.readlines()
	
		files = len(list0)/37
		print ("Files=" + str(files))
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
			if mtype==0:
				dire[i] = dire[i] + "Pics/Cropped_pics/"
			else: 
				dire[i] = dire[i] + "Density_pics/"
			
			if name[i].find('Pw_') >= 0:
				if (name[i])[-6:-4] == '10':
					continue
				else:
					if mtype==0:
						name[i] = 'cr_' + name[i][:-4] + '.png'
					else:
						name[i] = name[i] + '_' + str(resol) +'.png'
					
			else:
				if mtype==0:
					name[i] = 'cr_' + name[i] + '.png'
				else:
					name[i] = name[i] + '_' + str(resol) +'.png'
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
			t_nmctr[index] = t_nmctr[index] + 1
			aver[6] = aver[6] + x
	
			# predict takes any number of images,
			# and formats them for the Caffe net automatically
			transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
			transformer.set_mean('data', mu)
			transformer.set_transpose('data', (2,0,1))
			transformer.set_channel_swap('data', (2,1,0))
			transformer.set_raw_scale('data', 255)
			if mtype ==0 : 
				net.blobs['data'].reshape(1,3,372,372)
			else: 
				net.blobs['data'].reshape(1,3,256,256)
			im = caffe.io.load_image(path1)
			#print (name[i] + ": " + str(im.shape))
			net.blobs['data'].data[...] = transformer.preprocess('data', im)
			out = net.forward()
			output_prob = out['prob'][0]
			top_k = output_prob.argsort()[::-1][:6]
		
			if top_k[0]==index or top_k[1] == index:
				r2_pred = r2_pred + 1
			if top_k[0]==index:
				r_pred = r_pred + 1
				t_pred[top_k[0]] = t_pred[top_k[0]] + 1
		
			pred[top_k[0]] = pred[top_k[0]] + 1
			rec_pred[top_k[0]] = rec_pred[top_k[0]] + 1
			
			#print ( "Prediction: " + str(top_k[0]) + " or " + str(top_k[1])  + " vs actual " + str(index) + " (" + str(r_pred) + "/" + str(total_files) + ")")	
			aver[7] = aver[7] + max1[top_k[0]]
		for k in range(0,len(nm)):
			print  ( nm[k] + " Average =  %.3f"  %(aver[k]/total_files) + " GB/s" )
		print  ("Ideal Average =  %.3f"  %(aver[6]/total_files) + " GB/s" )
		print  ("\nPredicted Average =  %.3f"  %(aver[7]/total_files) + " GFLOPs/s" )		

		print (str(close_perf) + " implementations were closer than " + str(prec*100) + "%")
		Acc[dirctr] = round((1.0*r_pred/total_files),2)
		Acc_top2[dirctr] = round((1.0*r2_pred/total_files),2)
		dirctr = dirctr + 1
		print ("Average stats for " + str(total_files) + " arrays:	")
		#for i in range(0, len(nm)):
		#	print  (nm[i] + ": Average =  %.3f"  %(aver[i]/total_files) + " GFLOPs/s" )
		for i in range(0, len(pred)):
			print  ('Predicted: ' + nm[i] + "= " + str(pred[i]) + "/" +str(total_files) )
			print  ('Actual: ' + nm[i] + "= " + str(nmctr[i]) + "/" +str(total_files) )
		print ( 'Acc = ' + str(Acc[dirctr-1]) + ' Acc_top2 = ' + str(Acc_top2[dirctr-1])  )
		if model == models[0]:
			outstr[dirctr+1] = outstr[dirctr+1] + ' & ' + str(total_files) 
			outstr1[dirctr+1] = outstr1[dirctr+1] + ' & ' + str(total_files)
			for k in range(0, len(t_nmctr)):
				outstr2[k + 2] = outstr2[k + 2] + ' & ' + str(t_nmctr[k]) 

		t_total = t_total + total_files
		outstr[dirctr+1] = outstr[dirctr+1] + ' & ' + str(Acc[dirctr-1]) + ' & ' + str(Acc_top2[dirctr-1]) 
		outstr1[dirctr+1] = outstr1[dirctr+1] + ' & ' + str(round(aver[7]/aver[0],2)) + ' & ' + str(round(aver[6]/aver[0],2)) 
		print ( outstr[dirctr+1])
		print ( outstr1[dirctr+1])
	outstr[0] = outstr[0] + ' & ' + model.split('/')[-1] 
	outstr1[0] = outstr1[0] + ' & ' + model.split('/')[-1] 	
	outstr2[0] = outstr2[0] + ' & ' + model.split('/')[-1] 
	outstr[1] = outstr[1] + '& Acc. & Top 2 Acc. '
	outstr1[1] = outstr1[1] + '& Predicted & Maximum '
	outstr2[1] = outstr2[1] + ' & Acc. '
	for k in range(0, len(t_nmctr)):
		outstr2[k + 2] = outstr2[k + 2] + ' & ' + str(round(1.0*t_pred[k]/t_nmctr[k],2))
		if model == models[-1]:
			if t_pred[k] == 0 or rec_pred[k]==0:
				outstr2[k + 2] = outstr2[k + 2] + ' & ' + '0.00'
			else:
				outstr2[k + 2] = outstr2[k + 2] + ' & ' + str(round(1.0*t_pred[k]/rec_pred[k],2))
	print ( 'Model Recall: ')
	for k in range(0, len(rec_pred)):
		if t_pred[k] == 0 or rec_pred[k]==0:
			print (0.00)
		else:
			print(round(1.0*t_pred[k]/rec_pred[k],2))

for i in range(0, len(vpath_list) + 2):
	if i < 3 or i > len(vpath_list):
		print ('\hline')
	print  outstr[i] + ' \\\\'
print ('\hline')	
print ( '\nPerformance')
for i in range(0, len(vpath_list) + 2):
	if i < 3 or i > len(vpath_list):
		print ('\hline')
	print  outstr1[i] + ' \\\\'
print ('\hline')	
for i in range(0, len(nm) + 2):
	if i < 3 or i > len(nm):
		print ('\hline')
	print  outstr2[i] + ' \\\\'
print ('\hline')		
