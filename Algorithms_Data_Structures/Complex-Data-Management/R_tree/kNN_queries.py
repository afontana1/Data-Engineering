# Apostolis Kasselouris, A.M:2994

# python version 3.8.5

import sys
import json
import math
from queue import PriorityQueue

R = [] #the R tree list

K = 0  				#K Nearest Neighbors
line_counter = 0 	#number of line(query) we are counter


# yields lines of a file as objects
def parser(fname):
	for line in fname.readline().strip().split(" "):
		yield line

# returns next lines values of a file as a list
def next_row(fd):
	line_obj = parser(fd)
	lst = []
	for num in line_obj:
		lst.append(num)
		
	try:
		# returns a float type list
		return list(map(float, lst))
	except ValueError:
		# if ValueError because of empty list return empty list with no conversion to float
		return lst


#calculates the nearest distance between a querys point and a mbrs rectangle 
def calculate_distance(point, mbr):
	#calculate dx
	if(point[0] < mbr[0]):
		dx = mbr[0] - point[0]
	elif(point[0] > mbr[1]):
		dx = point[0] - mbr[1]
	else:
		dx = 0

	#calculate dy
	if(point[1] < mbr[2]):
		dy = mbr[2] - point[1]
	elif(point[1] > mbr[3]):
		dy = point[1] - mbr[3]
	else:
		dy = 0

	#return distance
	return math.sqrt(dx**2 + dy**2)


#Best First Nearest Neighbor Search
def bf_nn_search(query, node):
	global line_counter

	priority_queue = PriorityQueue()	#initialize a min Priority Queue class
	nn_counter = 0	#counts the nearest neigbors number we have find so far
	nn_list = []	#stores the K nearest neighbors for a querys point

	#add all entries of R tree root nodes to priority queue
	for entry in node[2]:
		distance = calculate_distance(query, entry[1])
		priority_queue.put((distance, entry[0], 1))
		#tuple is of type (min_distance_mbr_from_point, entry_node_id, entry_type(0 or 1))

	#get the K nearest neighbors for a querys point
	while(nn_counter < K):
		nn = get_next_bf_nn_search(query, priority_queue)
		nn_list.append(nn)
		nn_counter += 1

	#print results
	print(str(line_counter)+": " + ', '.join(map(str, nn_list)))
	line_counter += 1
	

def get_next_bf_nn_search(query, priority_queue):
	while not priority_queue.empty():
		#get min query node tuple(min_distance_mbr_from_point, entry_node_id, entry_type(0 or 1)
		#Note: entry_type = 1 if entry is node of a directory node
		# else entry_type = 0 if entry is an object of a leaf node
		min_node_tuple = priority_queue.get()	#based on tuples first element min
		min_node_id = min_node_tuple[1]		#get id
		min_node_entry = min_node_tuple[2]	#get entry type

		if(min_node_entry == 1):	#node
			min_node = R[min_node_id]		#get node based on id

			if(min_node[0] == 1):		#directory node entry
				for entry in min_node[2]:
					distance = calculate_distance(query, entry[1])
					priority_queue.put((distance, entry[0], 1))
			else:						#leaf
				for entry in min_node[2]:
					distance = calculate_distance(query, entry[1])
					priority_queue.put((distance, entry[0], 0))
		else:						#object
			return min_node_id	#return nearest neighbor id


def build_Rtree(Rtree):
	global R
	Rtree_raw = Rtree.readlines()
	
	for node in Rtree_raw:
		# convert a node from a string to a list
		R.append(json.loads(node))
	Rtree_raw.clear()


def main(args):
	global K

	if not(len(args) == 4):
		print("Error: Wrong number of arguments.")
		print("Try: python3 kNN_queries.py Rtree.txt NNqueries.txt k(nearest neighbors)")
		sys.exit(1)

	Rtree = open(args[1], "r")
	NNqueries = open(args[2], "r")
	K = int(args[3])	#K Nearest Neighbors

	#build the R tree list
	build_Rtree(Rtree)

	#parse queries
	query = next_row(NNqueries) 
	while(len(query) > 1):
		bf_nn_search(query, R[-1])	#(query, root node)
		query = next_row(NNqueries) 

	Rtree.close()
	NNqueries.close()


if __name__ == '__main__':
	main(sys.argv)