#Sur les machines de l'INSA, installer networkx avec : https://networkx.github.io/documentation/stable/install.html
#Paragraphe "Install the development version" avec git : git clone https://github.com/networkx/networkx.git

import matplotlib.pyplot as plt
import networkx as nx


##### Generator + Drawing #####
#See https://networkx.github.io/documentation/latest/auto_examples/index.html

#Scale free graph generator : 
H = nx.barabasi_albert_graph(10, 5)
nx.draw(H)
plt.show()

#Différentes représentation d'un même graphe avec deux draw consécutifs : 
nx.draw(H)
plt.show()

#Small world graph generator + drawing nodes labels :
I = nx.newman_watts_strogatz_graph(20, 4, 0.15)
nx.draw(I, with_labels=True)
plt.show()

##### Using np.matrix #####
import numpy as np

#Example from https://networkx.github.io/documentation/stable/reference/convert.html#module-networkx.convert_matrix  Numpy section :
a = np.reshape(np.random.random_integers(0, 1, size=100), (10, 10))
D = nx.DiGraph(a)
nx.draw(D)
plt.show()

J = nx.path_graph(10)
nx.draw(J)
plt.show()
M = nx.to_numpy_matrix(J) #Options!
print (M)


'''
OUT :
[[0. 1. 0. 0. 0. 0. 0. 0. 0. 0.]
 [1. 0. 1. 0. 0. 0. 0. 0. 0. 0.]
 [0. 1. 0. 1. 0. 0. 0. 0. 0. 0.]
 [0. 0. 1. 0. 1. 0. 0. 0. 0. 0.]
 [0. 0. 0. 1. 0. 1. 0. 0. 0. 0.]
 [0. 0. 0. 0. 1. 0. 1. 0. 0. 0.]
 [0. 0. 0. 0. 0. 1. 0. 1. 0. 0.]
 [0. 0. 0. 0. 0. 0. 1. 0. 1. 0.]
 [0. 0. 0. 0. 0. 0. 0. 1. 0. 1.]
 [0. 0. 0. 0. 0. 0. 0. 0. 1. 0.]]
'''

#From matrix to graph : The numpy matrix is interpreted as an adjacency matrix for the graph
m = np.matrix('0 1 0 0 0 0 0 0 0 0; 1 0 1 0 0 0 0 0 0 0; 0 1 0 1 0 0 0 0 0 0; 0 0 1 0 1 0 0 0 0 0; 0 0 0 1 0 1 0 0 0 0; 0 0 0 0 1 0 1 0 0 0; 0 0 0 0 0 1 0 1 0 0; 0 0 0 0 0 0 1 0 1 0; 0 0 0 0 0 0 0 1 0 1; 0 0 0 0 0 0 0 0 1 0')
K = nx.from_numpy_matrix(m)
nx.draw(K)
plt.show()


#Génération d'un graphe, passage en matrice, modifications, retour en graphe
x = 10
N = nx.barabasi_albert_graph(x, 2)
nx.draw(N, with_labels = True)
plt.show()
M = nx.to_numpy_matrix(N)
print(M)
#On supprime toutes les arrêtes : 
for i in range(x) :
	for j in range(x) : 
		M[i,j] = 0
Nprime = nx.from_numpy_matrix(M)
nx.draw(Nprime, with_labels = True)
plt.show()

