import numpy as np
import random
import math
import pickle as pk
from prettytable import PrettyTable

def iniciar_valores_MK(x_values,k = 2):
	mk = []
	for i in range(k):
		mi = x_values[random.randint(0,(len(x_values)-1))]
		mk.append(mi)
	return mk	

def clustering(x_values,iterations,k = 2):
	m = len(x_values)
	centroids = []
	mk = iniciar_valores_MK(x_values)
	cn = []
	for i in range(m):
		cn.append(0)
	for j in range(iterations):
		for i in range(m):
			cn[i] = Buscar_Cercano(x_values[i],mk)
		mk = Puntos_MK(cn,x_values)
		centroids.append(np.array(cn))
	return centroids

def Puntos_MK(centroids, x_values, k = 2):
	mks = []
	for i in range(k):
		mks.append([])

	for i in range(len(centroids)):
		mks[centroids[i]].append(x_values[i])

	for i in range(k):
		aux = np.array(mks[i])
		if len(aux) == 0:
			mks[i] = np.array([x_values[random.randint(0,(len(x_values)-1))]])
		
	for i in range(k):
		aux = np.array([])
		for j in range(len(mks[i])):
			if j == 0:
				aux = mks[i][j]
			else:
				aux = aux + mks[i][j]
		mks[i] = aux/len(mks[i])
	return mks

def Buscar_Cercano(xi, mk):
	index = 0
	for i in range(len(mk)):
		aux = Distancia(xi, mk[i])
		if i == 0:
			d = aux
		else:
			if d > aux:
				d = aux
				index = i
	return index

def Distancia(x1, x2):
	d = (x1 - x2) ** 2
	return math.sqrt(d.sum())

def Errores(clusters, y_values,tags):
    t= ["  ","Mensajes SPAM","Mensajes HAM"]
    tag=["Real","Cluster 1","Cluster 2"]
    tabla= PrettyTable(t)
    tabla.add_row([tag[0],str(y_values.count(1)),str(y_values.count(0))])
    tabla.add_row([tag[1],str(clusters[0][tags[1]]),str(clusters[0][tags[0]])])
    tabla.add_row([tag[2],str(clusters[1][tags[1]]),str(clusters[1][tags[0]])])
    print(tabla)

def Numeros_Totales_de_Clusters(centroids, tags):
	clusters = []
	for i in range(len(centroids)):
		numbers = {}
		for tag in tags:
			numbers[tag] = 0
		clusters.append(numbers)

	for i in range(len(centroids)):
		for value in centroids[i]:
			clusters[i][tags[value]] = clusters[i][tags[value]] + 1

	return clusters

if __name__ == '__main__':
	fx = open("vectores_x.bit","rb")
	x_valores = pk.load(fx)
	fx.close()
	fy = open("vectores_y.bit","rb")
	y_valores = pk.load(fy)
	fy.close()
	centroids = clustering(x_valores,2)
	tags = ["ham","spam"]
	clusters = Numeros_Totales_de_Clusters(centroids, tags)
	Errores(clusters,y_valores,tags)
