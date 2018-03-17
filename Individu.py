#coding: utf8
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import powerlaw

#Importation du graphe de base et de ses caracteristiques
Fb = nx.read_edgelist('facebook_combined.txt')
Deg_dist_ref = nx.degree_histogram(Fb)
Deg_prob_ref = np.array(Deg_dist_ref)/float(np.sum(np.array(Deg_dist_ref)))
Alpha_ref = powerlaw.Fit(Deg_prob_ref).power_law.alpha #Parametre de la loi de puissance de la distribution des degrees du graphe de reference

'''
N_ref = np.sum(Deg_dist_ref) #Nb de noeuds
CC_ref = nx.average_clustering(Fb)
DI_ref = nx.diameter(Fb)
'''
N_ref = 4039 #Nb de noeuds
CC_ref = 0.6055
DI_ref = 8



class Individu:
	def __init__(self, TYPE, N):
		if TYPE == "SW":
			G = nx.newman_watts_strogatz_graph(N, 4, 0.50)
		if TYPE == "Random":
			G = nx.gnm_random_graph(N,5)
		if TYPE == "SF":
			G = nx.barabasi_albert_graph(N, 5)

		self.CC = nx.average_clustering(G)
		self.DI = nx.diameter(G)
		self.DD = nx.degree_histogram(G)
		self.W = 1
		self.N = N
		self.matrix = nx.to_numpy_matrix(G)

	def prattribut(self):
		print "Matrice d'adjacence :\n", (self.matrix)
		print "CC", self.CC
		print "Diamètre :", self.DI
		print "Distribution des degres :", self.DD
		print "Fitness", self.W
		
		
	def Maj_attributs(self):
		Graph = nx.from_numpy_matrix(self.matrix)
		self.CC = nx.average_clustering(Graph)
		self.DI = nx.diameter(Graph)
		self.DD = nx.degree_histogram(Graph)
		
	
	def Maj_Fitness(self):
		'''
		#On ajuste la taille des deux liste en ajoutant des 0 dans la plus petite :
		diff_taille = len(Deg_dist_ref)-len(self.DD)
		if diff_taille > 0:
			for i in range(diff_taille):
				self.DD.append(0)
		else:
			for i in range(diff_taille):
				Deg_dist.append(0)
		
		
		#On calcule la différence de degrés par rapport au graphe de reférence
		Diff_DD = 0
		for i in range(len(self.DD)):
			Diff_DD = Diff_DD + (self.DD[i] - Deg_dist_ref[i])**2

		print Diff_DD
		'''
		#Diff_CC = (CC_ref - self.CC)**2
		#Diff_DI = (DI_ref - self.DI)**2
		
		wCC = min([CC_ref, self.CC])/max([CC_ref, self.CC]) #Fitness du coefficient de clustering
		wDI = float(min([DI_ref, self.DI]))/max([DI_ref, self.DI]) #Fitness du diametre
		DD_prob = np.array(self.DD)/float(np.sum(self.DD))
		Alpha = powerlaw.Fit(DD_prob).power_law.alpha #Coefficiant de la loi de puissance de la distribution des degres
		wDD = min([Alpha, Alpha_ref])/max([Alpha, Alpha_ref]) #Fitness de la distribution des degres (en passant par la comparaison des lois de puissance)
		
		self.W = (wCC + wDI + wDD)/3 #FITNESS TOTALE
		
		'''
		wDD = 0
		for i in range(len(Deg_dist_ref)):
			if max([self.DD[i], Deg_dist_ref[i]]) != 0:
				wDD +=  float(min([self.DD[i], Deg_dist_ref[i]]))/max([self.DD[i], Deg_dist_ref[i]])
				wDD = wDD * len(Deg_dist_ref)
		
		print self.DD, Deg_dist_ref
		print "3 fitness :", wCC, wDI, wDD
		
		self.W = wCC/3 + wDI/3 + wDD/3
		'''
	def mutation(self):   #Fonction de mutation, on change un lien d'amitié sur l'individu sélectionné
		print type(self.matrix)
		i,j = np.random.randint(0,self.N,2)
		if self.matrix[i,j] == 0:
			self.matrix[i,j] = 1
			self.matrix[i,j] = 1
		elif self.matrix[i,j] == 1:
			self.matrix[i,j] = 0
			self.matrix[i,j] = 1
			


#TESTS
'''
I = Individu("SW", 30)
I.Maj_Fitness()
I.prattribut()
I.mutation()
I.Maj_attributs()
I.Maj_Fitness()
I.prattribut()
'''
