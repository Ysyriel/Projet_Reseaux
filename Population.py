#coding: utf8
#Paul test
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

from Individu import *

class Population:
	def __init__(self, nb, TYPE, N):
		self.pop = []
		self.nb = nb
		self.N = N
		for i in range(nb): 
			self.pop.append(Individu(TYPE,  N))
			
	def pmatrix(self): #Affiche les matrices de l'ensemble des graphes de la population
		for i in range(len(self.pop)):
			print "Graphe %d:\n" %i, self.pop[i].matrix
		
	
	def selection(self):
		list_W = [] #liste des fitness pour chaque individu
		pioche = [] #liste de la "pioche", selon le fitness d'un individu son indice sera représenté plus ou moins de fois dans cette liste.
		for i in range(self.nb):
			list_W.append(self.pop[i].W) #Ajout des fitness pour chaque individu 
		W_total = np.sum(list_W)
		for i,j in enumerate(list_W) :
			nombre = (j/W_total)*100 #On crée le poids relatif de chaque fitness (par rapport à la somme totale des fitness).
			pioche = np.concatenate([pioche,np.repeat(i,int(nombre))]) #Puis on incrémente la liste "pioche"
		self.pop = [self.pop[int(i)] for i in np.random.choice(pioche,self.nb,replace=True)] #Et on remet à jour la nouvelle pop de nb individus à partir des nb indices de "pioche".

		
	def mutation(self):
		indice = np.random.randint(1,1000) # Proba de 1/1000 qu'un individu mute
		if indice < self.nb:
			self.pop[indice].mutation() #Fonction mutation appelée dans Individus
	
	
	def Crossing_over(self):
		g1, g2 = np.random.choice(self.nb, 2, replace = False) #Selection des 2 individus
		I1, I2 = np.random.choice(self.N+1, 2, replace = False) #Selection de la portion de la matrice à interchanger
		i1 = min(I1, I2)
		i2 = max(I1, I2)
		print g1, g2
		print i1, i2
		i1, i2 = 0,10
		
		#STOCKAGE
		c1 = np.matrix(self.pop[g1].matrix[:,i1:i2])
		c2 = np.matrix(self.pop[g2].matrix[:,i1:i2])
		l1 = np.matrix(self.pop[g1].matrix[i1:i2,:])
		l2 = np.matrix(self.pop[g2].matrix[i1:i2,:])
		#REMPLACEMENT
		self.pop[g1].matrix[:,i1:i2] = c2
		self.pop[g1].matrix[i1:i2,:] = l2
		self.pop[g2].matrix[:,i1:i2] = c1
		self.pop[g2].matrix[i1:i2,:] = l1
		


P = Population(2, "SF", 10)

#Run de test 

print 'Test mises à jours de la population'
for temps in range(5):
	print "AU TEMPS",temps
	for ind in P.pop :   #1) On calcule les fitness pour chaque individu
		ind.Maj_Fitness()
	P.selection()   #2) Selection des individus
	P.Crossing_over() #3) Crossing overs sur les individus sélectionnés
	P.mutation() #4) Mutation éventuelle
	for ind in P.pop :   #1) Mise à jours des attributs
		ind.Maj_attributs()
		ind.prattribut()
	print "=========================================================="

