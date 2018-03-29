#coding: utf8

from Individu import *
import matplotlib.pyplot as plt
import time
import operator

class Population:
	def __init__(self, nb_individus, graph_type, ind_size):
		self.nb_individus = nb_individus
		self.ind_size = ind_size
		self.pop = []  # Contiendra tous les individus
		for i in range(nb_individus): 
			self.pop.append(Individu(graph_type,  ind_size))

	def __str__(self):  # Ce qui sera affiché si on print juste P
		return "Taille de la population : {} \nTaille des individus : {}".format(self.nb_individus, self.ind_size)


	def display(self,*args): # Affiche les matrices de l'ensemble des graphes de la population et/ou la fitness
		if "matrix" in args:
			for i in range(len(self.pop)):
				print "Graphe %d : \n " %i, self.pop[i].matrix
		if "fitness" in args:
			W_list = []
			for ind in range(self.nb_individus):
				W_list.append(self.pop[ind].W)
			print "FITNESS :", W_list
			print "FITNESS MOYENNE :", np.sum(W_list) / self.nb_individus
	
	def Maj_attributs(self):
		for ind in range(self.nb_individus) : 
			self.pop[ind].maj_attributs()
			
	def Maj_fitness(self):
		for ind in range(self.nb_individus) : 
			self.pop[ind].maj_fitness()
		
	def ponderation(self):
		list_W = [o.W for o in self.pop]  # Liste des fitness
		print 'FITNESS : ',list_W
		W_total = np.sum(list_W)  # Somme des fitness
		return [Wi/W_total for Wi in list_W]  # Vecteur de poids pour la population à l'instant t

	def roulette(self,poids):  # Resort 2 individus parents avec plus forte proba pour les meilleures fitness
		# print 'POIDS : ', poids
		papa, maman = np.random.choice(self.pop,2,p=poids)
		# print 'PAPA : ', papa.W, 'MAMAN : ', maman.W
		return papa, maman  # Oui bon désolé pour le raccourci, on va dire que pour faire des enfants il faut un papa et une maman

	def crossing_over2(self): # FONCTION BIDON A MODIFIER
		return self.pop[-1]

	def selection(self, proba_crossing_over = 0.8):
		n = int(proba_crossing_over*self.nb_individus)  # Où n est le nombre de crossing-over
		m = self.nb_individus - n  # Où m est le nombre d'individus gardés à l'identique
		self.pop.sort(key=operator.attrgetter('W'), reverse=True)  # Trie par fitness ; plus rapide que sorted puisque pas de nouvelle liste créée
		poids = self.ponderation()
		for i in range(n):  # Pour créer les n enfants
			papa, maman = self.roulette(poids)
			enfant = self.crossing_over2()  # Faire la fonction crossing over2
			self.pop[i+m] = enfant  # On renouvelle les n moins bons individus dans la population
		# print [o.W for o in self.pop]  # On vérifie que la population a bien été renouvelée
		# Intéressant à savoir : si on veut récupérer les n meilleurs d'une liste on peut voir ce lien : https://docs.python.org/3/library/heapq.html#heapq.nlargest

	def mutation(self):
		indice = np.random.randint(1,1000) # Proba de 1/1000 qu'un individu mute
		if indice < self.nb_individus:
			self.pop[indice].mutation() #Fonction mutation appelée dans Individus

	def Crossing_over(self):
		g1, g2 = np.random.choice(self.nb_individus, 2, replace = False) #Selection des 2 individus
		I1, I2 = np.random.choice(self.ind_size+1, 2, replace = False) #Selection de la portion de la matrice à interchanger
		i1 = min(I1, I2)
		i2 = max(I1, I2)
		
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

		


'=========================================================================================================='
'						DECLARATION DES VARIABLES ET INSTANCIATION DE LA POPULATION'
'=========================================================================================================='

taille_population = 10
taille_individus = 10
nb_it = 1
P = Population(taille_population, "SW", taille_individus)
list_best_fitness = []

'=========================================================================================================='
'												RUN DE TEST'
'==========================================================================================================' 
### TEST POUR SELECTION :
print '\n------------> Test mise à jour de la population <------------'
fit = P.selection()


# print '\n------------> Test mise à jour de la population <------------'
# print P  # Fait appel à la méthode spéciale __str__
# for temps in range(nb_it):
# 	# print "AU TEMPS",temps,"/",nb_it
# 	# P.pop[0].prattribut()
# 	# P.display("fitness","matrix")
# 	fit = P.selection()   #2) Selection des individus --> return liste des fitness de chaque individu
# 	list_best_fitness.append(max(fit))  # Pour suivre l'évolution des fitness au cours des itérations
# 	P.Crossing_over() #3) Crossing overs sur les individus sélectionnés
# 	P.Maj_attributs()
# print(list_best_fitness)
#	plt.plot(range(len(list_best_fitness)), list_best_fitness)
#	plt.show()
# print "=========================================================="
# print "TEMPS :", time.time() - t0


# #Test crossing over
# for i in range(4):
# 	print 'TEMPS :', i
# 	P.Pfitness()
# 	P.Maj_fitness()
# 	P.Pfitness()


#print "TEMPS :", time.time() - t0

# for i in range(20):
# 	print "AU TEMPS :", i
# 	P.Pmatrix()
# 	P.Crossing_over()

'=========================================================================================================='
'								RUN DE TEST POUR ENREGISTREMENT DANS FICHIER'
'==========================================================================================================' 
# for i in range(10):
# 	for taille_population in range(10,51):
# 		for taille_individus in range(20,21):
# 			for nb_it in [1]: # Linéarité prouvée et logique
# 				t0 = time.time()
# 				P = Population(taille_population, "SW", taille_individus)
# 				gene = time.time()-t0
# 				t0 = time.time()
# 				list_best_fitness = []
# 				for t in range(nb_it):
# 					fit = P.selection()
# 					selec = time.time()-t0
# 					t0 = time.time()
# 					list_best_fitness.append(max(fit))
# 					bestfit = time.time()-t0
# 					t0 = time.time()
# 					P.Crossing_over()
# 					crosover = time.time()-t0
# 					t0 = time.time()
# 					P.Maj_attributs()
# 					majattrib = time.time()-t0
# 					t0 = time.time()
# 					P.Maj_fitness()
# 					majfit = time.time()-t0
# 					t0 = time.time()
# 					print taille_population, '\t', taille_individus, '\t', gene,'\t', selec, '\t', bestfit, '\t', crosover, '\t', majattrib, '\t', majfit
# 			#print taille_population, '\t', taille_individus, '\t', nb_it, '\t', time.time()-t0

' Pour créer un fichier propre dans le répertoire parent... '
' ...écrire dans le terminal : echo -e "T_pop \t T_ind \t Nb_it \t Temps" > ../Gestion_Projet_Reseau/resultats_250318_1.txt '
' Pour lancer l enregistrement dans le bon fichier : python Population.py >> ../Gestion_Projet_Reseau/resultats_250318_1.txt '
' Les ">>" servent à écrire dans le fichier sans écraser '
