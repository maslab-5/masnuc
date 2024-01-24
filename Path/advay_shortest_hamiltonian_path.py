from sys import maxsize 
from itertools import permutations
import math

import numpy as np

def segments_distance(x11, y11, x12, y12, x21, y21, x22, y22):
	if segments_intersect(x11, y11, x12, y12, x21, y21, x22, y22):
		return 0
	# try each of the 4 vertices w/the other segment
	distances = []
	distances.append(point_segment_distance(x11, y11, x21, y21, x22, y22))
	distances.append(point_segment_distance(x12, y12, x21, y21, x22, y22))
	distances.append(point_segment_distance(x21, y21, x11, y11, x12, y12))
	distances.append(point_segment_distance(x22, y22, x11, y11, x12, y12))
	return min(distances)

def segments_intersect(x11, y11, x12, y12, x21, y21, x22, y22):
	""" whether two segments in the plane intersect:
	one segment is (x11, y11) to (x12, y12)
	the other is   (x21, y21) to (x22, y22)
	"""
	dx1 = x12 - x11
	dy1 = y12 - y11
	dx2 = x22 - x21
	dy2 = y22 - y21
	delta = dx2 * dy1 - dy2 * dx1
	if delta == 0: return False  # parallel segments
	s = (dx1 * (y21 - y11) + dy1 * (x11 - x21)) / delta
	t = (dx2 * (y11 - y21) + dy2 * (x21 - x11)) / (-delta)
	return (0 <= s <= 1) and (0 <= t <= 1)

import math
def point_segment_distance(px, py, x1, y1, x2, y2):
	dx = x2 - x1
	dy = y2 - y1
	if dx == dy == 0:  # the segment's just a point
		return math.hypot(px - x1, py - y1)

	# Calculate the t that minimizes the distance.
	t = ((px - x1) * dx + (py - y1) * dy) / (dx * dx + dy * dy)

	# See if this represents one of the segment's
	# end points or a point in the middle.
	if t < 0:
		dx = px - x1
		dy = py - y1
	elif t > 1:
		dx = px - x2
		dy = py - y2
	else:
		near_x = x1 + t * dx
		near_y = y1 + t * dy
		dx = px - near_x
		dy = py - near_y

	return math.hypot(dx, dy)

def make_graph(startX, startY, stacks, walls):
	robot_width = 0.6
	def wall_in_way(v1, v2):
		for wall in walls:
			dist = segments_distance(v1[0], v1[1], v2[0], v2[1], wall[0][0], wall[0][1], wall[1][0], wall[1][1])
			if dist < robot_width/2:
				return True
		return False




	G = {}
	G[(startX, startY)] = {}
	for stack in stacks:
		X, Y = stack[0], stack[1]
		G[(X,Y)] = {}

	for v1 in G:
		for v2 in G:
			if v1 == v2:
				continue

			else:
				if not wall_in_way(v1, v2):
					G[v1][v2] = ((v1[0] - v2[0])**2 + (v1[1]-v2[1])**2)**0.5
					G[v2][v1] = ((v1[0] - v2[0])**2 + (v1[1]-v2[1])**2)**0.5
	return G

def travellingSalesmanProblem(graph, s): 

	# store all vertex apart from source vertex 
	vertex = [] 
	for v in graph:
		if v != s: 
			vertex.append(v) 
	# store minimum weight Hamiltonian Cycle 
	min_length  = float('inf')
	min_path = None
	next_permutation=permutations(vertex)
	for i in next_permutation:
	# store current Path weight(cost) 
		current_pathweight = 0

			# compute current path weight 
		finished = True
		curr = s 
		for j in i: 
			if j not in graph[curr]:
				finished = False
				break
			else:
				current_pathweight += graph[curr][j]
				curr = j  
		if not finished:
			continue
		if current_pathweight < min_length:
			min_length = current_pathweight
			min_path = i
	return (min_path, min_length)

startX= 0.5
startY= 0.5
stacks= [[1.0, 2.0, [False, True, False]], [2.0, 1.0, [False, True, False]], [3.0, 3.0, [False, True, False]], [4.0, 4.0, [False, True, False]], [5.0, 3.0, [False, True, False]]]
walls= [[[0, 1.5], [1,1.5]],[[1.0, 5.0], [6.0, 5.0]], [[6.0, 5.0], [6.0, 2.0]], [[6.0, 2.0], [5.0, 2.0]], [[5.0, 2.0], [5.0, 1.0]], [[5.0, 1.0], [3.0, 1.0]], [[3.0, 1.0], [3.0, 0.0]], [[3.0, 0.0], [0.0, 0.0]], [[0.0, 0.0], [0.0, 3.0]], [[0.0, 3.0], [1.0, 3.0]], [[1.0, 3.0], [1.0, 5.0]]]
G = make_graph(startX, startY, stacks, walls)
#print(segments_distance(0,10,1,10,0,0,1,0))
print(travellingSalesmanProblem(G, (startX, startY)))