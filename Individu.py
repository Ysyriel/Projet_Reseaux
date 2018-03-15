#coding: utf8
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

Fb = nx.read_edgelist('facebook_combined.txt')
Deg_dist_ref = nx.degree_histogram(Fb)
N_ref = np.sum(Deg_dist_ref)
CC_ref = nx.average_clustering(Fb)
DI_ref = nx.diameter(Fb)

print N_ref


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
		Degres = np.array(nx.degree_histogram(G))
		self.DD = nx.degree_histogram(G)
		
		self.matrix = nx.to_numpy_matrix(G)

	def prattribut(self):
		print "Matrice d'adjacence :", (self.matrix)
		print "CC", self.CC
		print "Diamètre :", self.DI
		print "Distribution des degres :", self.DD
		
	def Maj_Fitness(self):
		#On ajuste la taille des deux liste en ajoutant des 0 dans la plus petite :
		diff_taille = len(Deg_dist_ref)-len(self.DD)
		if diff_taille > 0:
			for i in range(diff_taille):
				self.DD.append(0)
		else:
			for i in range(diff_taille):
				Deg_dist.append(0)
		
		#On calcule la différence de degrés par rapport au graphe de refférence
		Diff_DD = 0
		for i in range(len(self.DD)):
			Diff_DD = Diff_DD + (self.DD[i] - Deg_dist_ref[i])**2

		print Diff_DD


I = Individu("SW", 20)
I.Maj_Fitness()
#I.prattribut()
