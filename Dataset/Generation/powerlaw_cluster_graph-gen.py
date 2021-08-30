import matplotlib.pyplot as plt
import os
import scipy as sci
import scipy.sparse as spa
from scipy import io
import numpy as np
import random
import math
from scipy import stats
import networkx as nx

def spyplot(x, str1):
	plt.spy(x, marker= '.', markersize=0.01)
	plt.axis('off')
	plt.savefig(str1 +'.png')
	plt.close()

def freescale(nodes, dm):
	I = []
	J = []
	M = [0]*nodes*dm*2
	for i in range(0,nodes):
		for j in range(0,dm):
			M[2*(i*dm+j)] = i
			I.append(i)
			r = int( random.random()* 2*(i*dm+j) )
			M[2*(i*dm+j) + 1] = M[r]
			J.append(M[r])
	S = [1]*nodes*dm*2
	K1 = I + J
	K2 = J + I
	A = spa.coo_matrix((S,( K1, K2)), shape = (nodes, nodes))
	K1 = []
	K2 = []
	S = []
	for i in range(0,A.nnz):
		if A.row[i] != A.col[i]:
			K1.append(A.row[i])
			K2.append(A.col[i])
			S.append(A.data[i])
	return spa.coo_matrix((S,( K1, K2)), shape = (nodes, nodes))

p_triangle = 0.1
dest = '/local/panastas/powerlaw_cluster/'

for nodes in range(300000, 400001, 10000):
	for edge_num in [2,4,6,8,10]:
		for ran in range(0,10):
			G = nx.powerlaw_cluster_graph(nodes, edge_num, p_triangle)
			A = nx.to_scipy_sparse_matrix(G)	
			density = 1.0*A.nnz/(A.shape[0]*A.shape[1])
			spyplot(A, dest + 'Pics/'+ 'Pw_cl_graph_' + str(nodes) + '_' + str(edge_num) + '_' + str(ran))
			io.mmwrite(dest + 'Pw_cl_graph_' + str(nodes) + '_' + str(edge_num) + '_' + str(ran+1), A, comment = 'A Matrix produced from nx.powerlaw_cluster_graph with ' + str(nodes) + ', Edge_num= ' + str(edge_num) + 'p= ' + str(p_triangle))
			print ('Pw_cl_graph_' + str(nodes) + '_' + str(edge_num) + '_' + str(ran) +': nnz= ' + str( A.nnz ) +', density= '+ str( density )  )








