#coding: utf8

from Individu import *
import time


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
		
	
	def selection(self):
		list_W = [] #liste des fitness pour chaque individu
		poids = [] #liste de la "pioche", selon le fitness d'un individu son indice sera représenté plus ou moins de fois dans cette liste.
		individus = []
		for i in range(self.nb_individus):
			list_W.append(self.pop[i].W) #Ajout des fitness pour chaque individu 
		W_total = np.sum(list_W)
		for i,j in enumerate(list_W) :
			poids.append(j/W_total)
			individus.append(i)
			#pioche = np.concatenate([pioche,np.repeat(i,int(nombre))]) #Puis on incrémente la liste "pioche"
		#self.pop = [self.pop[int(i)] for i in np.random.choice(pioche,self.nb_individus,replace=True)] #Et on remet à jour la nouvelle pop de nb_individus individus à partir des nb_individus indices de "pioche".
		self.pop = [self.pop[int(i)] for i in np.random.choice(individus,self.nb_individus,poids)]
		#print self.Pmatrix()
		return list_W

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

# taille_population = 10
# taille_individus = 10
# nb_it = 1
# P = Population(taille_population, "SW", taille_individus)
# list_best_fitness = []

'=========================================================================================================='
'												RUN DE TEST'
'==========================================================================================================' 

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
# print(list_best_fitness) # Ça servira quand la fitness fonctionnera...
# print "=========================================================="
# print "TEMPS :", time.time() - t0

'''
#Test crossing over
for i in range(20):
	print "AU TEMPS :", i
	P.Pmatrix()
	P.Crossing_over()
'''
'=========================================================================================================='
'								RUN DE TEST POUR ENREGISTREMENT DANS FICHIER'
'==========================================================================================================' 
for taille_population in range(10,50,10):
	for taille_individus in range(10,50,10):
		for nb_it in [1,10,100,250,500,1000]:
			t0 = time.time()
			P = Population(taille_population, "SW", taille_individus)
			list_best_fitness = []
			for t in range(nb_it):
				fit = P.selection()
				list_best_fitness.append(max(fit))
				P.Crossing_over()
				P.Maj_attributs()
			print taille_population, '\t', taille_individus, '\t', nb_it, '\t', time.time()-t0

' Pour créer un fichier propre dans le répertoire parent... '
' ...écrire dans le terminal : echo -e "T_pop \t T_ind \t Nb_it \t Temps" > ../resultats_250318_1.txt '
' Pour lancer l enregistrement dans le bon fichier : python Population.py >> ../resultats_250318_1.txt '
' Les ">>" servent à écrire dans le fichier sans écraser '
