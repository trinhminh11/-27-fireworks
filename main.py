from random import *
from math import *
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import timeit
import collections	
import yaml

from CONSTANT import *
from Q_Connectivity import *
from Q_Coverage import *

Dataset = [n, 40, 80]
print(Dataset)
base = [0, 0, 0]

class Vertex(object):
	def __init__(self, v, q, index):
		self.v = v
		self.neigh = []
		self.q = q
		self.index = index
		self.p = None

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


def Cluster(T, Rs, Q):
	C = []

	n = len(T)
	parent = [i for i in range(n)]


	V = [Vertex(T[i], Q[i], i) for i in range(n)]
	E = []
	for i in range(n-1):
		for j in range(i+1, n):
			if dist(V[i].v, V[j].v) <= 2*Rs:
				if find_set(i, parent) == find_set(j, parent):
					continue
				union_sets(i, j, parent)

	for i in range(n):
		V[i].p = find_set(i, parent)

	V.sort(key = lambda x: x.p)
	minp = V[0].p
	maxp = V[-1].p
	Vindex = 0
	for p in range(minp, maxp+1):
		C.append([])

		while Vindex < n and V[Vindex].p == p:
			C[p-minp].append(V[Vindex])
			Vindex += 1

	temp = C.count([])
	for i in range(temp):
		C.remove([])

	return C

def Plot2D(T,S,Rn,path,base,size, name):
	fig, ax = plt.subplots()

	G = [base] + S + Rn
	for i in range(len(path)):
		A = G[path[i][0]]
		B = G[path[i][1]]

		plt.plot([A[0], B[0]], [A[1], B[1]], c = "g")

	# plt.scatter(base[0], base[1], c="purple", marker = image, label = 'base')

	x,y,z = [T[i][0] for i in range(len(T))], [T[i][1] for i in range(len(T))], [T[i][2] for i in range(len(T))]
	plt.scatter(x, y, c='r', label='Targets', marker = "*")

	x,y,z = [S[i][0] for i in range(len(S))], [S[i][1] for i in range(len(S))], [S[i][2] for i in range(len(S))]
	plt.scatter(x, y, c='b', label='Sensors')

	x,y,z = [Rn[i][0] for i in range(len(Rn))], [Rn[i][1] for i in range(len(Rn))], [Rn[i][2] for i in range(len(Rn))]
	plt.scatter(x, y, c='orange', label='Relay nodes')
	

	# Generate the sphere data
	# R = data["Rs"]
	# u = np.linspace(0, 2 * np.pi, 100)
	# v = np.linspace(0, np.pi, 100)
	# x = R * np.outer(np.cos(u), np.sin(v))
	# y = R * np.outer(np.sin(u), np.sin(v))
	# z = R * np.outer(np.ones(np.size(u)), np.cos(v))

	# for point in T:
	# 	ax.plot_surface(x + point[0], y + point[1], z + point[2], color='green', alpha=0.5)

	plt.legend(loc = "upper right")
	plt.xlim(0, size)
	plt.ylim(0, size)

	plt.xlabel('X')
	plt.ylabel('Y')


	plt.title(name)
	plt.show()

def Plot(T,S,Rn,path,base,size, name):

	Tz = [T[i][2] for i in range(len(T))]

	ax = plt.figure().add_subplot(projection='3d')

	x,y,z = [T[i][0] for i in range(len(T))], [T[i][1] for i in range(len(T))], [T[i][2] for i in range(len(T))]
	ax.scatter(x, y, z, c='r', label='Targets', marker = "*")

	x,y,z = [S[i][0] for i in range(len(S))], [S[i][1] for i in range(len(S))], [S[i][2] for i in range(len(S))]
	ax.scatter(x, y, z, c='b', label='Sensors')

	x,y,z = [Rn[i][0] for i in range(len(Rn))], [Rn[i][1] for i in range(len(Rn))], [Rn[i][2] for i in range(len(Rn))]
	ax.scatter(x, y, z, c='orange', label='Relay nodes')

	ax.scatter(base[0], base[1], base[2], c = "black", label = "base")
	G = [base] + S + Rn


	for i in range(len(path)):
		A = G[path[i][0]]
		B = G[path[i][1]]

		ax.plot([A[0], B[0]], [A[1], B[1]], [A[2], B[2]], c = "g")

	# Generate the sphere data
	# R = data["Rs"]
	# u = np.linspace(0, 2 * np.pi, 100)
	# v = np.linspace(0, np.pi, 100)
	# x = R * np.outer(np.cos(u), np.sin(v))
	# y = R * np.outer(np.sin(u), np.sin(v))
	# z = R * np.outer(np.ones(np.size(u)), np.cos(v))

	# for point in T:
	# 	ax.plot_surface(x + point[0], y + point[1], z + point[2], color='green', alpha=0.5)

	ax.legend()
	ax.set_xlim(0, size)
	ax.set_ylim(0, size)
	ax.set_zlim(min(Tz), max(Tz))

	ax.set_xlabel('X')
	ax.set_ylabel('Y')
	ax.set_zlabel('Z')


	plt.title(name)
	plt.show()

def main(file, H, n):
	data = {}
	base = [H//2, H//2, 0]
	data['base_station'] = [base[0], base[1]]
	with open(f"data\\{file}.asc", "r") as f:
		f.readline()
		f.readline()
		xllcorner = float(f.readline()[9:-1])
		yllcorner = float(f.readline()[9:-1])
		cellsize = float(f.readline()[8:-1])
		NODATA_value = f.readline()
		data_asc = f.readlines()
		data_asc[0] = data_asc[0][13:]
		data_asc[0] = list(map(float, data_asc[0].split()))
		for i in range(1, len(data_asc)):
			data_asc[i] = list(map(float, data_asc[i].split()))
			data_asc[i-1].append(data_asc[i].pop(0))
		data_asc.pop()
		cell = int(H//25)
		data_asc = data_asc[-cell:]
		for i in range(len(data_asc)):
			data_asc[i] = data_asc[i][:cell]

	data['xllcorner'] = xllcorner
	data['yllcorner'] = yllcorner

	T = []
	Rs = Dataset[1]
	data['Rs'] = Rs
	Rc = Dataset[2]
	data['Rc'] = Rc

	Q = [1 for i in range(n)]

	for k in range(n):
		x, y = random()*H, random()*H
		z = data_asc[int(x//25)][int(y//25)]
		T.append((x,y,z))

	Targets = {'targets': []}
	for i in range(len(T)):
		Targets['targets'].append([T[i][0], T[i][1]])
	Tz = [T[i][2] for i in range(len(T))]
	base[2] = (min(Tz) + max(Tz))/2

	C = Cluster(T, Rs, Q)
	GS = []
	S = []
	Tc = []
	Qc = []
	for k in range(len(C)):
		Tc.append([])
		Qc.append([])
		for j in range(len(C[k])):
			Tc[k].append(C[k][j].v)
			Qc[k].append(C[k][j].q)

	for k in range(len(C)):
		Sq, Gq = Q_Coverage(Tc[k], Rs, Qc[k])
		S += Sq
		GS += Gq

	Nodes = {"nodes": []}
	for i in range(len(S)):
		Nodes['nodes'].append([float(S[i][0]), float(S[i][1])])

	Vs, Rn = Q_Connectivity(base, GS, Rc)

	for i in range(len(Rn)):
		Nodes["nodes"].append([float(Rn[i][0]), float(Rn[i][1])])



	G = [base] + S + Rn

	G = Kruskal(G)

	Plot(T,S,Rn,G,base,H, file)


	names_yaml = """# multiple nodes charging model
node_phy_spe:
  "capacity" : 10800
  "threshold" : 540
  "com_range": 80
  "sen_range": 40
  "prob_gp": 1
  # others
  "package_size" : 400.0
  # transmission specifications
  "er" : 0.0001
  "et" : 0.00005
  "efs" : 0.00000001
  "emp" : 0.0000000000013

seed: 0

"""
	# names = yaml.safe_load(names_yaml)
	# with open(f"data\\{file}{H}n{n}.yaml", "w") as f:
	# 	yaml.dump(names, f)
	# 	yaml.dump(data, f)
	# 	yaml.dump(Nodes, f)
	# 	yaml.dump(Targets, f)



main(file, H, n)
