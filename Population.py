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
		for i in range(nb): 
			self.pop.append(Individu("SW",  20))
		
	
	def selection(self):
		list_W = [] #liste des fitness pour chaque individu
		pioche = [] #liste de la "pioche", selon le fitness d'un individu son indice sera représenté plus ou moins de fois dans cette liste.
		for i in range(self.nb):
			list_W.append(self.pop[i].W) #Ajout des fitness pour chaque individu
			print 
		W_total = np.sum(list_W)
		for i in list_W :
			nombre = (i/W_total)*100 #On crée le poids relatif de chaque fitness (par rapport à la somme totale des fitness).
			np.concatenate([pioche,np.repeat(i,nombre)]) #Puis on incrémente la liste "pioche"
		self.pop = self.pop[np.random.choice(pioche,self.nb,replace=True)] #Et on remet à jour la nouvelle pop de nb individus à partir des nb indices de "pioche".

		
	def mutation(self):
		indice = np.random.randint(1,1000) # Proba de 1/1000 qu'un individu mute
		if indice < self.nb:
			self.pop[indice].mutation() #Fonction mutation appelée dans Individus


P = Population(50, "SW", 20)
P.pop[0].prattribut()
P.pop[49].prattribut()

print 'Test de malade'
P.selection()
P.pop[49].prattribut()
