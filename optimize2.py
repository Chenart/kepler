from random import randint
from math import sin, cos, acos, radians


# desparate attempt at optimization
tilt_factors = [[[0 for i in range(361)] for j in range(91)] for k in range(181)]

for theta1 in range(181):
	for theta2 in range(91):
		for phi in range(361):
			tilt_factors[theta1][theta2][phi] = cos(radians(theta1))*cos(radians(theta2)) + sin(radians(theta1))*sin(radians(theta2))*cos(radians(phi))
num_orbits = int(raw_input())


# The idea is to check every point on the Earth and see if it is covered by a ring in order
# to find the maximum coverage area. But this would either be way too slow or the orbits would
# just be oriented so that the swaths end up between the points we check. So instead, every time we call fitness,
# we take a random sample of 200 points and check how many are covered. Yes, the result eventually does converge.
def fitness(rings):
	total = 0

	points = [[randint(0,180), randint(0,360)] for i in range(200)]
	for point in points:
		for ring in rings:
			# acceptable range on angles based on 350 x 350 km satellite coverage area
			if abs(tilt_factors[point[0]][ring[0]][abs(point[1] - ring[1])]) <= 0.02746476134:
				total += 1
				break
	return total

def new_parent():
	return [[0, 0]] + [[randint(0,90), randint(0,359)] for i in range(num_orbits - 1)]

def mutate(parent):
	parent[randint(1,len(parent) - 1)][0] = randint(0, 90)
	parent[randint(1,len(parent) - 1)][1] = randint(0, 359)
	return parent

def quiver(parent):
	a = randint(1,len(parent) - 1)
	b = randint(1,len(parent) - 1)
	parent[a][0] += randint(-1, 1)
	parent[a][0] = max(parent[randint(1,len(parent) - 1)][0], 0)
	parent[a][0] = min(parent[randint(1,len(parent) - 1)][0], 90)
	parent[b][1] += randint(-1, 1)
	parent[b][1] = max(parent[randint(1,len(parent) - 1)][1], 0)
	parent[b][1] = min(parent[randint(1,len(parent) - 1)][1], 359)
	return parent

def mate(parent1, parent2):
	child = parent1
	for i in range(len(parent1)):
		if randint(0, 1) == 0:
			child[i] = parent2[i]
	return child

population_size = 50
parents = []
for i in range(population_size):
	parent = new_parent()
	parents += [[fitness(parent), parent]]

while True:
	try:
		parents.sort(reverse=True)
		print parents[0][0], parents[-1][0]

		children = [parents[0], parents[1]]
		for i in range(5):
			walk = quiver(parents[0][1])
			children += [[fitness(walk), walk]]

		for i in range(5):
			walk = quiver(parents[1][1])
			children += [[fitness(walk), walk]]

		for i in range(population_size - 12):
			# all the children are from the strongest two parents
			child = mate(parents[0][1], parents[1][1])

			# mutate one in 10 to prevent getting stuck in a local minimum
			should_mutate = randint(0, 5)
			if should_mutate == 3:
				child = mutate(child)
			children += [[fitness(child), child]]
		parents = children
	except:
		print sorted(parents[0][1])
		print parents[0][0]
		quit()
print sorted(parents[0][1])
print parents[0][0]
