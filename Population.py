#coding: utf8

from Individu import *
import matplotlib.pyplot as plt
import time
import operator
import matplotlib.pyplot as plt

class Population:
	def __init__(self, nb_individus, graph_type, ind_size):
		CC_ref = 10000
		self.nb_individus = nb_individus
		self.ind_size = ind_size
		self.pop = []  # Contiendra tous les individus
		for i in range(nb_individus): 
			self.pop.append(Individu(graph_type, ind_size))
		
		#liste des fitness moyennes incrementée chaque pas de temps
		self.WMOY = []
		self.WMOY_CC = []
		self.WMOY_DI = []
		self.WMOY_DD = []
		
		self.Maj_fitness()	

	def __str__(self):  # Ce qui sera affiché si on print juste P
		return "Taille de la population : {} \nTaille des individus : {}".format(self.nb_individus, self.ind_size)

	def display(self,*args): # Affiche les matrices de l'ensemble des graphes de la population et/ou la fitness
		if "matrix" in args:
			for i in range(len(self.pop)):
				print "Graphe %d :" %i
				self.pop[i].display("matrix")
		if "fitness" in args:
			W_list = []
			for ind in range(self.nb_individus):
				W_list.append(self.pop[ind].W)
			print "FITNESS :", W_list
		if "fitness_moy" in args:
			print "FITNESS MOYENNE :", self.Wmoy
		if "fitness_coeffs" in args:
			print "fitness CC :", self.WCCmoy
			print "fitness DI :", self.WDImoy
			print "fitness DD :", self.WDDmoy
	
			
	def Maj_fitness(self):
		#Fitness globale et des coeffs cumulées
		WCCcumul = float(0)
		WDIcumul = float(0)
		WDDcumul = float(0)
		Wcumul = float(0)
		
		for ind in range(self.nb_individus) : 
			Wcumul += self.pop[ind].maj_fitness() #Met a jour les fitness des individus
			WCCcumul += self.pop[ind].wCC
			WDIcumul += self.pop[ind].wDI
			WDDcumul += self.pop[ind].wDD
		
		#fitness globale et des coeffs moyennes
		self.Wmoy = Wcumul/self.nb_individus
		self.WCCmoy = WCCcumul/self.nb_individus
		self.WDImoy = WDIcumul/self.nb_individus
		self.WDDmoy = WDDcumul/self.nb_individus
		
		#Sauvegarde des fitness moyennes
		self.WMOY.append(self.Wmoy)
		self.WMOY_CC.append(self.WCCmoy)
		self.WMOY_DI.append(self.WDImoy)
		self.WMOY_DD.append(self.WDDmoy)
		
	def ponderation(self):
		list_W = [o.W for o in self.pop]  # Liste des fitness
		# print 'FITNESS : ',list_W
		W_total = np.sum(list_W)  # Somme des fitness
		return [Wi/W_total for Wi in list_W]  # Vecteur de poids pour la population à l'instant t

	def roulette(self,poids):  # Ressort 2 individus parents avec plus forte proba pour les meilleures fitness
		# print 'POIDS : ', poids
		papa, maman = np.random.choice(self.pop,2,p=poids, replace=False)
		# print 'PAPA : ', papa.W, 'MAMAN : ', maman.W
		return papa, maman  # Oui bon désolé pour le raccourci, on va dire que pour faire des enfants il faut un papa et une maman

	def crossing_over(self, G1, G2): #Prend 2 graphes parents en argument en retourne un graph enfant
		n1 = rn.randint(self.ind_size/4,3*self.ind_size/4) #Nombre de noeuds provenant du graphe 1 choisis aleatoirement
		Noeuds1 = rn.sample(list(G1.G.nodes), n1) #Liste des noeuds de n1 choisis
		Noeuds2 = []
		for n in range(self.ind_size): #Remplissage de la liste des noeuds provenant de G2
			if n not in Noeuds1:
				Noeuds2.append(n)
				
		#print "noeuds du g1 :", Noeuds1
		#print "noeuds du g2 :", Noeuds2
		
		Edges = [] #Liste des edges des noeuds de G1
		for noeud in Noeuds1:
			for e in list(G1.G.edges(noeud)):
				Edges.append(e)
		Edges2 = [] #Liste des edges des noeuds de G2
		for noeud in Noeuds2:
			for e in list(G2.G.edges(noeud)):
				Edges2.append(e)
		
		G3 = Individu("NONE", self.ind_size) #Initialisation du graph enfant
		G3.G.add_nodes_from(G1.G) #Possede le meme nombre de noeuds que les graphes parents
		G3.G.add_edges_from(Edges) #Prend les edges de G1
		G3.G.add_edges_from(Edges2) # Prend les edges de G2
		
		#Met a jour les attributs et la fitness du graph
		G3.maj_attributs()
		G3.maj_fitness()
		#print "G3 : ",G3.CC, G3.DI, G3.DD

		return G3 #Retourne le graph enfant

	def selection(self, proba_crossing_over = 0.70):
		n = int(proba_crossing_over*self.nb_individus)  # Où n est le nombre de crossing-over
		m = self.nb_individus - n  # Où m est le nombre d'individus gardés à l'identique
		self.pop.sort(key=operator.attrgetter('W'), reverse=True)  # Trie par fitness ; plus rapide que sorted puisque pas de nouvelle liste créée
		#print self.pop[0].W
		poids = self.ponderation()
		for i in range(n):  # Pour créer les n enfants
			papa, maman = self.roulette(poids)
			enfant = self.crossing_over(papa, maman)
			self.pop[i+m] = enfant  # On renouvelle les n moins bons individus dans la population
		# print [o.W for o in self.pop]  # On vérifie que la population a bien été renouvelée
		# Intéressant à savoir : si on veut récupérer les n meilleurs d'une liste on peut voir ce lien : https://docs.python.org/3/library/heapq.html#heapq.nlargest


	def mutation(self, p): #proba de p qu'un individu mute
		h = rn.random()
		if h < p:
			indice = rn.randint(0,self.nb_individus - 1) #Selection de l'individu muté
			self.pop[indice].mutation() #Fonction mutation appelée dans Individus
			
			
	def run(self, n, p_mut = 0.01, portion_crossing_over = 0.5): #n nombre d'iterations
		Fichier = open('Resultats_%dI_%dN.txt'%(self.nb_individus, self.ind_size), 'a') #Creation du fichier
		Fichier.write("Taille individu : %d \n Taille population : %d \n Proba mutation : %f \n Frequence des graphs à subir un crossing : %f \n" %(
		self.ind_size, self.nb_individus, p_mut, portion_crossing_over))
		
		for i in range(n):
			print "Iteration ",i+1,"/",n," :"
			self.selection(portion_crossing_over)
			self.mutation(p_mut)
			self.Maj_fitness()
			self.display("fitness_moy", "fitness_coeffs")
			Fichier.write("Iteration %d : \n Fitness moyenne : %f \n Fit_CC : %f \n Fit_DI : %f \n Fit_DD : %f \n \n"%(i+1, self.Wmoy, self.WCCmoy, self.WDImoy, self.WDDmoy))
			if ((i+1)%10 == 0):
				plt.plot(self.WMOY)
				plt.plot(self.WMOY_CC)
				plt.plot(self.WMOY_DI)
				plt.plot(self.WMOY_DD)
				plt.legend(["glob", "CC", "DI", "DD"], loc=2)
				plt.savefig('Plot__%dI_%dN_%dit.png'%(self.nb_individus, self.ind_size, i+1), bbox_inches='tight')
				plt.show()
				
				
		plt.plot(self.WMOY)
		plt.plot(self.WMOY_CC)
		plt.plot(self.WMOY_DI)
		plt.plot(self.WMOY_DD)
		plt.legend(["glob", "CC", "DI", "DD"], loc=2)
		plt.savefig('Plot__%dI_%dN_%dit.png'%(self.nb_individus, self.ind_size, n), bbox_inches='tight')
		plt.show()





'=========================================================================================================='
'						DECLARATION DES VARIABLES ET INSTANCIATION DE LA POPULATION'
'=========================================================================================================='


taille_population = 40
taille_individus = 30
nb_it = 15
t0 = time.time()
P = Population(taille_population, "SW", taille_individus)
print "Temps de génération de la population : ",time.time()-t0


'=========================================================================================================='
'												RUN DE TEST'
'==========================================================================================================' 
#RUN
t0 = time.time()
P.run(nb_it)
print "Temps d'execution des iterations : ", time.time()-t0



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
