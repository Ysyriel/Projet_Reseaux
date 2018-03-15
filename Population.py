#coding: utf8
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

from Individu import *

class Population:
	def __init__(self, nb, TYPE, N):
		self.pop = []
		for i in range(nb): 
			self.pop.append(Individu("SW",  20))
		
	
P = Population(50, "SW", 20)
P.pop[0].prattribut()
P.pop[49].prattribut()

