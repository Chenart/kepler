from random import randint
from math import sin, cos, acos, radians

num_orbits = 6 

def fitness(rings):
	total = 0
	for i in range(len(rings)):
		for j in range(i + 1, len(rings)):
			theta1 = radians(rings[i][0])
			phi1 = radians(rings[i][1])
			theta2 = radians(rings[j][0])
			phi2 = radians(rings[j][1])

			tilt_factor = cos(theta1)*cos(theta2) + sin(theta1)*sin(theta2)*cos(phi1 - phi2)
			if tilt_factor >= 1 or tilt_factor <= -1:
				return 100000000000
			else:
				total += 1.0/sin(acos(tilt_factor))
	return total

def new_parent():
	return [[0, 0]] + [[randint(0,179), randint(0,179)] for i in range(num_orbits - 1)]

def mutate(parent):
	parent[randint(1,len(parent) - 1)][randint(0, 1)] = randint(0, 179)
	return parent

def mate(parent1, parent2):
	child = parent1
	for i in range(len(parent1)):
		if randint(0, 1) == 0:
			child[i] = parent2[i]
	return child

population_size = 30
parents = []
for i in range(population_size):
	parent = new_parent()
	parents += [[fitness(parent), parent]]
print parents

while True:
	try:
		parents.sort()
		print parents[0][0], parents[-1][0]

		children = [parents[0], parents[1]]
		if parents[-1][0] - parents[0][0] < 0.0000001:
			break
		for i in range(population_size - 2):
			# all the children are from the strongest two parents
			child = mate(parents[0][1], parents[1][1])

			# mutate one in 10 to prevent getting stuck in a local minimum
			should_mutate = randint(0, 10)
			if should_mutate == 5:
				child = mutate(child)
			children += [[fitness(child), child]]
		parents = children
	except:
		print sorted(parents[0][1])
		print parents[0][0]
		quit()
print sorted(parents[0][1])
print parents[0][0]
