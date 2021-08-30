import sys
sys.path.append("/home/users/athena/caffe/python")
import caffe
import lmdb
import numpy as np
from  PIL import Image
from caffe.proto import caffe_pb2
# Wei Yang 2015-08-19
# Source
#   Read LevelDB/LMDB
#   ==================
#       http://research.beenfrog.com/code/2015/03/28/read-leveldb-lmdb-for-caffe-with-python.html
#   Plot image
#   ==================
#       http://www.pyimagesearch.com/2014/11/03/display-matplotlib-rgb-image/
#   Creating LMDB in python
#   ==================
#       http://deepdish.io/2015/04/28/creating-lmdb-in-python/

lmdb_file = "/home/users/panastas/Training_material/Neural_data/Testing_data/val_lmdb"
lmdb_env = lmdb.open(lmdb_file)
lmdb_txn = lmdb_env.begin()
lmdb_cursor = lmdb_txn.cursor()
datum = caffe_pb2.Datum()
num = 0

MODEL_FILE = '../caffe_train/Arch/Googlenet/deploy.prototxt'
PRETRAINED = '../Solverstates/My_googlenet_iter_60000.caffemodel'
mu = np.zeros(3)
print 'mean-subtracted values:', zip('BGR', mu)

def is_non_zero_file(fpath):  
	return os.path.isfile(fpath) and os.path.getsize(fpath) > 0

caffe.set_mode_gpu()


#net = caffe.Classifier(MODEL_FILE, PRETRAINED, )
net = caffe.Net(MODEL_FILE,PRETRAINED, caffe.TEST)
print ("successfully loaded Net")

for key, value in lmdb_cursor:
	path = ('/local/panastas/' + key.split('/')[3] + '/Density_pics/')
	path1 = path + key.split('/')[-1]
	print (path1)
	transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
	transformer.set_mean('data', mu)
	transformer.set_transpose('data', (2,0,1))
	transformer.set_channel_swap('data', (2,1,0))
	transformer.set_raw_scale('data', 255)
	net.blobs['data'].reshape(1,3,256,256)
	im = caffe.io.load_image(path1)
	net.blobs['data'].data[...] = (transformer.preprocess('data', im)).astype(np.uint8)

	datum.ParseFromString(value)
	label = datum.label
	data = caffe.io.datum_to_array(datum)
	im = data.astype(np.uint8)
	img = Image.open(path1)
	print (data)
	print (net.blobs['data'].data[...])
