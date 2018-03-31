#coding: utf8

#coding: utf8

import networkx as nx
import matplotlib.pyplot as plt
import time
import random as rn
import numpy as np
from louispuissance import *

Fb = nx.read_edgelist('facebook_combined.txt') #graph

t0 = time.time()

#La fonction average clustering est plus lente
'''
Clusts = nx.clustering(Fb).values()
print sum(Clusts)/float(len(Clusts))
t1 = time.time() - t0
print "T1 :", t1

print nx.average_clustering(Fb)

t2 = time.time() - (t0+t1)
print "T2 :", t2
'''


#Test la vitesse de conversion graph > matrice > graph
'''
for i in range(50):
	mat = nx.to_numpy_matrix(Fb)
	fb = nx.from_numpy_matrix(mat)
	
t1 = time.time() - t0
print "T1 :", t1
'''


#Temps de calcul des coeffs


#CLUSTERING COEFF
Clusts = nx.clustering(Fb).values()
print sum(Clusts)/float(len(Clusts))
t1 = time.time() - t0
print "CC :", t1

#DISTRIBUTION DES DEGRES
DD = nx.degree_histogram(Fb)
DD_prob = np.array(DD)/float(np.sum(DD))
print Fit(DD_prob).power_law.alpha
t2 = time.time() - (t0+t1)
print "alpha :", t2

#DIAMETRE
#DI = nx.diameter(Fb)
DI = nx.average_shortest_path_length(Fb)
print DI
t3 = time.time() - (t0+t1+t2)
print "DI :", t3
