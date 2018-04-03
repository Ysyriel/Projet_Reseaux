#coding: utf8
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from louispuissance import *
import sys
import random as rn

#Importation du graphe de base et de ses caracteristiques
Fb = nx.read_edgelist('facebook_combined.txt')
Deg_dist_ref = nx.degree_histogram(Fb)
Deg_prob_ref = np.array(Deg_dist_ref)/float(np.sum(np.array(Deg_dist_ref)))
Alpha_ref = Fit(Deg_prob_ref).power_law.alpha #Parametre de la loi de puissance de la distribution des degrees du graphe de reference

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
		if (TYPE != "SF" and TYPE != "Random" and TYPE != "SW" and TYPE != "NONE"):	
			sys.exit("ERREUR DE SAISIE DANS LE TYPE DU GRAPHE")
		if TYPE == "SW":
			self.G = nx.newman_watts_strogatz_graph(N, 4, 0.50)
		#if TYPE == "Random":
			#G = nx.complete_graph(N)
		if TYPE == "SF":
			self.G = nx.barabasi_albert_graph(N, 5)
		if TYPE == "NONE":
			self.G = nx.Graph()
			self.N = N
		
		if TYPE != "NONE":
			Clusts = nx.clustering(self.G).values()
			self.CC =  sum(Clusts)/float(len(Clusts))
			
			
			self.DI = nx.diameter(self.G)
			self.DD = nx.degree_histogram(self.G)
			self.W = 0
			self.maj_fitness()
			self.N = N
			#self.matrix = nx.to_numpy_matrix(self.G)

	def __str__(self):  # Ce qui sera affiché si on print juste Individu
		return "Fitness : {}".format(self.W)

	def display(self, *args):
		#print "Matrice d'adjacence :\n", (self.matrix) #Prend de la place...
		if "coeffs" in args:
			print "CC", self.CC
			print "Diamètre :", self.DI
			print "Distribution des degres :", self.DD
		if "fitness" in args:
			print "Fitness", self.W
		if "graph" in args:
			print "nodes :", self.G.nodes()
			print "edges :", self.G.edges()
		if "matrix" in args:
			print nx.to_numpy_matrix(self.G)
			
		
	def maj_attributs(self):
		Clusts = nx.clustering(self.G).values()
		self.CC =  sum(Clusts)/float(len(Clusts))
		self.DI = nx.diameter(self.G)
		self.DD = nx.degree_histogram(self.G)
		
	
	def maj_fitness(self):
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
		Alpha = Fit(DD_prob).power_law.alpha #Coefficient de la loi de puissance de la distribution des degres
		wDD = min([Alpha, Alpha_ref])/max([Alpha, Alpha_ref]) #Fitness de la distribution des degres (en passant par la comparaison des lois de puissance)
		
		self.W = ((wCC + wDI + wDD)/3) #FITNESS TOTALE
		
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
		return self.W


	def mutation(self):   #Fonction de mutation, on change un lien d'amitié sur l'individu sélectionné
		n1 = rn.randint(0,self.N-1) #Indice du noeud
		if len(list(self.G.edges(n1))) > 1:
			e = rn.choice(list(self.G.edges(n1))) #Choisi un des edges du noeud selectionné
			if self.G.degree(e[1]) > 1: #Si le 2e noeud du edge selectionne a plus de 2 edge
				self.G.remove_edge(e[0], e[1])
		


#TESTS
'''
I = Individu("SW", 8)
I.display("graph")
I.mutation()
I.display("graph")

I.mutation()
'''
