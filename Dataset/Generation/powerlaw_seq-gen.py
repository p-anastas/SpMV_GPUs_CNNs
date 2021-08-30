import matplotlib.pyplot as plt
import os
import scipy as sci
import scipy.sparse as spa
from scipy import io
import numpy as np
import math
import sys
from scipy import stats
import networkx as nx

def spyplot(x, str1):
	plt.spy(x, marker= '.', markersize=0.01)
	plt.axis('off')
	plt.savefig(str1 +'.png')
	plt.close()

def normalize(adj_arr,nod):
	K1 = []
	K2 = []
	S = []
	for n in range(0,B.nnz):
		K1.append( adj_arr.row[n] - nod)
		K2.append( adj_arr.col[n] - nod)
		S.append( adj_arr.data[n] )
	return ( K1, K2, S)

dest = '/local/panastas/powerlaw_seq_graphs/'
if len (sys.argv) != 2:
	print ('Problem with input' )
else:
	pl = float(sys.argv[1])
	for nodes in range(200000, 500000, 10000):
		for ran in range(0,10):
			#create a graph with degrees following a power law distribution
			s = nx.utils.powerlaw_sequence(nodes, pl)
			G = nx.expected_degree_graph(s, selfloops=False)
			A = nx.to_scipy_sparse_matrix(G)
			if spa.issparse(A):
				B = spa.coo_matrix(A)
				(K1,K2,S) = normalize(B,nodes)
				A = spa.coo_matrix( (S, (K1,K2)))	
				density = 1.0*A.nnz/(A.shape[0]*A.shape[1])
				spyplot(A, dest + 'Pics/'+ 'Pw_seq_graph_' + str(nodes) + '_' + str(pl) + '_' + str(ran))
				io.mmwrite(dest + 'Pw_seq_graph_' + str(nodes) + '_' + str(pl) + '_' + str(ran+1), A, comment = 'A Matrix produced from nx.utils.powerlaw_sequence with ' + str(nodes) + ', Pl_exp= ' + str(pl))
				print ('Pw_cl_graph_' + str(nodes) + '_' + str(pl) + '_' + str(ran) +': nnz= ' + str( A.nnz ) +', density= '+ str( density )  )
			else:
				print ( 'Pw_cl_graph_' + str(nodes) + '_' + str(pl) + '_' + str(ran+1) + ' is not sparse' )

