import numpy as np
import matplotlib.pyplot as plt
def ImportData(file, H):
	with open(f"{file}.asc", "r") as f:
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
			data_asc[i] = data_asc[i][-cell:]
	return data_asc

def Plot(file, H):
	data_asc = ImportData(file, H)


	ax = plt.figure().add_subplot(projection='3d')

	_x = [25*i for i in range(len(data_asc))]
	_y = [25*i for i in range(len(data_asc))]
	_xx, _yy = np.meshgrid(_x, _y)
	x, y = _xx.ravel(), _yy.ravel()

	top = []

	
	bottom = np.zeros_like(top)
	width = depth = 25

	minx = []
	maxx = []

	for i in range(len(data_asc)):
		minx.append(min(data_asc[i]))
		maxx.append(max(data_asc[i]))

	for i in range(len(data_asc)):
		for j in range(len(data_asc[i])):
			top.append(data_asc[i][j]-min(minx))

	bottom = [min(minx) for i in range(len(top))]
	ax.bar3d(x, y, bottom, width, depth, top, shade=True)

	ax.set_xlim(0, H)
	ax.set_ylim(0, H)
	ax.set_zlim(min(minx), max(maxx))

	ax.set_xlabel('X')
	ax.set_ylabel('Y')
	ax.set_zlabel('Z')


	plt.show()

Plot('sonla', 2500)


# n = [300:700] step = 50