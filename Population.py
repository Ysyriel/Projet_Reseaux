#coding: utf8

from Individu import *
import time

t0 = time.time()

class Population:
	def __init__(self, nb_individus, graph_type, nb_it):
		self.nb_individus = nb_individus
		self.nb_it = nb_it
		self.pop = []  # Contiendra tous les individus
		for i in range(nb_individus): 
			self.pop.append(Individu(graph_type,  nb_it))

	def __str__(self):  # Ce qui sera affiché si on print juste P
		return "Taille de la population : {} \nNombre d'itérations : {}".format(self.nb_individus, self.nb_it)


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

	def mutation(self):
		indice = np.random.randint(1,1000) # Proba de 1/1000 qu'un individu mute
		if indice < self.nb_individus:
			self.pop[indice].mutation() #Fonction mutation appelée dans Individus
	
	
	def Crossing_over(self):
		g1, g2 = np.random.choice(self.nb_individus, 2, replace = False) #Selection des 2 individus
		I1, I2 = np.random.choice(self.nb_it+1, 2, replace = False) #Selection de la portion de la matrice à interchanger
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
		


P = Population(5, "SW", 10)

#Run de test 

print '\n------------> Test mise à jour de la population <------------'
print P  # Fait appel à la méthode spéciale __str__
for temps in range(1):
	print "AU TEMPS",temps
	P.pop[0].prattribut()
	P.display("fitness")
	P.selection()   #2) Selection des individus
	P.Crossing_over() #3) Crossing overs sur les individus sélectionnés
	P.Maj_attributs()
	#P.Pfitness()
	print "=========================================================="


'''
#Test crossing over
for i in range(20):
	print "AU TEMPS :", i
	P.Pmatrix()
	P.Crossing_over()
'''


print "TEMPS :", time.time() - t0
