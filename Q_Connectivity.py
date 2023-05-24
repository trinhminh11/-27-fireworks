import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from CONSTANT import *
from random import *
import matplotlib.pyplot as plt
from math import *


def find_set(v, parent):

	if v == parent[v]: 
		return v
	p = find_set(parent[v], parent)
	parent[v] = p
	return p

def union_sets(a, b, parent):
	a = find_set(a, parent)
	b = find_set(b, parent)
	if (a != b):
		parent[b] = a


# kruskal algorithm
def Kruskal(S):
	ans = []
	E = []
	parent = [i for i in range(len(S))]

	for i in range(len(S)-1):
		for j in range(i+1, len(S)):
			E.append([dist(S[i], S[j]),i,j])

	E.sort()
	count = 0

	for i in range(len(E)):
		u = E[i][1]
		v = E[i][2]
		if find_set(u, parent) == find_set(v, parent):
			continue
		union_sets(u, v, parent)
		ans.append([u,v])
		count += 1
		if count == len(S)-1:
			break

	return ans
# O(mlog(m))

#Q_Connectivity Constraint
def Q_Connectivity(base, GS, Rc):
	#base: Coordinates of base
	#GS = {GS1, GS2, ..., GSm} which GSi = set of sensor that covered Target i
	#Rc: Radius of Relay Nodes

	# arange GS
	GS.sort(reverse = True, key = lambda x: len(x))
	for i in range(len(GS)):
		GS[i].sort()
		
	for i in range(1, len(GS)):
		j = 0
		while j < len(GS[i]):
			if GS[i][j] != 0:
				for k in range(i):
					if GS[i][j] in GS[k]:
						l = GS[k].index(GS[i][j])
						GS[i][j] = 0
						if l < len(GS[i]):
							GS[i][j], GS[i][l] = GS[i][l], GS[i][j]
							j-=1
						break
			j += 1

	# O(n^2*qmax)

	#devide paths
	paths = []
	for q in range(len(GS[0])):
		paths.append([])

		for i in range(len(GS)):
			if q >= len(GS[i]):
				break
			if GS[i][q] != 0:
				paths[q].append(GS[i][q])
	#O(n*qmax)


	Vs = []


	#do Kruskal for each path
	for q in range(len(GS[0])):
		Vs.append([[base]+paths[q], Kruskal([base]+paths[q])])
	#O(nlog(n)*qmax)

	#compute number of relay nodes
	Rn = []
	for q in range(len(Vs)):
		P = Vs[q][0]
		E = Vs[q][1]

		for i in range(len(Vs[q][0])-1):
			P1 = P[E[i][0]]
			P2 = P[E[i][1]]
			c = dist(P1, P2)
			add = int((c-1)//(Rc))

			for j in range(add):
				x = P1[0] + (j+1)*(P2[0]-P1[0])/(add+1)
				y = P1[1] + (j+1)*(P2[1]-P1[1])/(add+1)
				z = P1[2] + (j+1)*(P2[2]-P1[2])/(add+1)

				sensor = (x, y, z)
				Rn.append(sensor)

			
	#O(qmax*n)

	return Vs, Rn

#O(n^2*qmax)


def Plotdata(W, H, V, ans):
	plt.xlabel('width')
	plt.ylabel("height")
	plt.xlim(0, W)
	plt.ylim(0, H)
	
	plt.scatter(V[0], V[0], s = 50)
	for i in range(len(V)-1):
		plt.plot((V[ans[i][0]][0], V[ans[i][1]][0]), (V[ans[i][0]][1], V[ans[i][1]][1]), c = 'green')

		plt.scatter(V[i+1][0], V[i+1][1], s = 50)
	plt.show()

if __name__ == "__main__":
	pass
	W = 100
	H = 100
	S = []
	for i in range(10):
		x, y = random()*W, random()*H
		S.append([x, y])
	S = [[5,5]] + S
	S = [[5, 5], [99.51791436441336, 21.959897113184635], [48.985943890389514, 37.442045923923686], [15.638881643012038, 98.00343670106545], [21.320686514887267, 44.39058731340442], [50.683781957363735, 91.45248730475366], [46.26851572099535, 65.78394047433062], [71.86694022221933, 42.02309169201018], [87.74551484691392, 87.94373290117079], [9.039105788464951, 90.4455968342361], [8.155106458550222, 34.67972037056447], [1.9061905280613023, 68.64956722032402], [52.73039155019118, 82.04360086260519], [40.04043992716233, 86.759892646958], [23.006778503983362, 67.90413087350285], [95.36498550910188, 52.399026464750456], [5.823357570376464, 99.68932362939037], [55.26373145750827, 50.002604856775044], [61.50837437898653, 6.044341906897632], [80.13394847038839, 51.44352710965771], [75.01542811270096, 96.35934869055825]]
	print(len(S))
	ans = Kruskal(S)
	print(ans)
	# for i in range(1, len(V)):
	# 	print(V[i].v, V[i].prev.v)
	Plotdata(W, H, S, ans)
	# K_Connectivity()

