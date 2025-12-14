#Apostolis Kasselouris, A.M:2994

#python version 3.8.5

import sys
import math
import heapq

network_list = []
#A node is in its corresponding position on the list eg node with id=5 is in network_list[5] position
#A position is of type [[node_x_axis, node_y_axis, neighbor_node_id, L2_distance, neighbor_node_id, L2_distance, ...]


#yields lines of a file as objects
def parser(fname):
	for line in fname.readline().strip().split(' '):
		yield line

#returns next lines values of a file as a list
def next_row(fd):
	line_obj = parser(fd)
	lst = []
	for num in line_obj:
		#convert number to int or float accordingly
		try:
			num = int(num)
		except ValueError:
			try:
				num = float(num)
			except ValueError:
				return lst
		lst.append(num)
	return lst

def build_network(network):
	global network_list
	
	while(True):
		node = next_row(network)

		if(len(node) > 1):
			node.pop(0)	#pop the node id because we can find nodes from their corresponding position on the list
			network_list.append(node)
		else:
			network.close()
			break


#yields a tuple of a nodes (neighbor_node_id, L2_distance_of_neighbor_from_node) 
#for as many neigbhors as it has
def neighbors(node):
	counter = 0
	
	for pos in node:
		if((counter % 2 == 1) and (counter > 2)):
			yield id, pos

		id = pos
		counter += 1


#calculates the L2 distance of two nodes(usually a nodes distance from target node)
def nodes_distance(node, target):
	#coords of node
	node_x = network_list[node][0]
	node_y = network_list[node][1]

	#coords of target
	target_x = network_list[target][0]
	target_y = network_list[target][1]

	#return distance
	return math.sqrt(abs(target_x - node_x)**2 + abs(target_y - node_y)**2)


def dijkstra_Astar_SP(source, target, algorithm):
	total_node_visits = 0	#counter for total node visits during Dijkstra algorithm

	SPD = []		#Shortest Path Distance initialization for each node
	path = []		#Initialize Shortest path for each node(eg a path for a node may be [3,6,2,...])
	visited = []	#list that contains for each node if is visited or not(True or False type)
	#Important for above lists as well as with network_list the node is in the corresponding position of the lists
	#eg for node with id = 7 we can find if is visited with visited[7]. Same thing with all lists.
	#Also for SPD and path we store the shortest path and distance compared to source node(source compared to node_id)

	for node in network_list:
		SPD.append(math.inf)
		path.append([])
		visited.append(False)

	#Shortest Path Distance from source(node) to source(node) is set to 0(obviously XD)
	SPD[source] = 0

	if(algorithm == "D"):	#if Dijkstra
		#Initialize and insert to priority queue a tuple of type (SPD, node_id)
		priority_queue = [(SPD[source], source)]
		priority_dict = {source : SPD[source]}	#initialize priority_dict for faster remove time in priority_queue
	else:	#if A*
		#Initialize and insert to priority queue a tuple of type (SPD + L2 distance of source node from target, node_id)
		priority_queue = [(SPD[source] + nodes_distance(source, target), source)]
		priority_dict = {source : SPD[source] + nodes_distance(source, target)}	#initialize priority_dict for faster remove time in priority_queue
	
	while True:
		try:
			#get node_id with the shortest path distance
			node_id = heapq.heappop(priority_queue)[1]
		except IndexError:
			#if IndexError priority_queue is empty so we exit the while-loop
			break

		visited[node_id] = True
		total_node_visits += 1
		
		if(node_id == target):
			path[target].append(target)		#append target node to path
			return SPD[target], total_node_visits, path[target]

		for neighbor in neighbors(network_list[node_id]):
			neighbor_id = neighbor[0]
			weight = neighbor[1]	#L2 distance between node and its neighbor

			if not(visited[neighbor_id]):
				if(algorithm == "D"): #if Dijkstra
					if(SPD[neighbor_id] > SPD[node_id] + weight):
						SPD[neighbor_id] = SPD[node_id] + weight
						
						path[neighbor_id].clear()	#clear old path
						path[neighbor_id].extend(path[node_id])
						path[neighbor_id].append(node_id)
						
						#add or update neighbor_id on priority queue
						try:	#neighbro_id in priority_dict -> UPDATE
							old_SPD = priority_dict[neighbor_id]
							priority_queue.remove((old_SPD, neighbor_id))
							heapq.heapify(priority_queue)

							priority_dict[neighbor_id] = SPD[neighbor_id] 
							heapq.heappush(priority_queue, (SPD[neighbor_id], neighbor_id))
						except KeyError:	#neighbro_id NOT in priority_dict -> ADD
							priority_dict[neighbor_id] = SPD[neighbor_id] 
							heapq.heappush(priority_queue, (SPD[neighbor_id], neighbor_id))
				else:	#if A*
					if(SPD[neighbor_id] + nodes_distance(neighbor_id, target) > 
						SPD[node_id] + nodes_distance(node_id, target) + weight):

						SPD[neighbor_id] = SPD[node_id] + weight
						
						path[neighbor_id].clear()	#clear old path
						path[neighbor_id].extend(path[node_id])
						path[neighbor_id].append(node_id)

						#add or update neighbor_id on priority queue
						try:	#neighbro_id in priority_dict -> UPDATE
							old_SPD = priority_dict[neighbor_id]
							priority_queue.remove((old_SPD, neighbor_id))
							heapq.heapify(priority_queue)

							priority_dict[neighbor_id] = SPD[neighbor_id] + nodes_distance(neighbor_id, target)
							heapq.heappush(priority_queue, (SPD[neighbor_id] + nodes_distance(neighbor_id, target), neighbor_id))
						except KeyError:	#neighbro_id NOT in priority_dict -> ADD
							priority_dict[neighbor_id] = SPD[neighbor_id] + nodes_distance(neighbor_id, target)
							heapq.heappush(priority_queue, (SPD[neighbor_id] + nodes_distance(neighbor_id, target), neighbor_id))


#check if source_node_id and target_node_id are VALID nodes
def check_validity(source, target):
	if(source < 0 or source >= len(network_list)):
		print("Error: Source_node_ID not found!")
		print("Enter a number from 0 to", len(network_list)-1)
		sys.exit(1)
	if(target < 0 or target >= len(network_list)):
		print("Error: Target_node_ID not found!")
		print("Enter a number from 0 to", len(network_list)-1)
		sys.exit(1)

def print_stats(results, source, target, algorithm):
	if(algorithm == "D"):	#dijkstra
		print("Dijkstra algorithm statistics for path from node "+ str(source) +" to node "+ str(target) +":")
	else:	#A*
		print("A* algorithm statistics for path from node "+ str(source) +" to node "+ str(target) +":")
	print("Shortest path length =", len(results[2]))
	print("Shortest path distance =", results[0])
	print("Shortest path =", results[2])
	print("Number of visited nodes =", results[1], "\n")


def main(args):
	if not(len(args) == 4):
		print("Error: Wrong number of arguments.")
		print("Try: python3 shortest_path.py out.txt source_node_ID target_node_ID")
		sys.exit(1)

	network = open(args[1], "r")
	source_node_id = int(args[2])
	target_node_id = int(args[3])
	
	#build the network_list
	build_network(network)

	#check if source_node_id and target_node_id are VALID nodes
	check_validity(source_node_id, target_node_id)
	
	dijkstra = dijkstra_Astar_SP(source_node_id, target_node_id, "D")	#call with dijkstra("D") parameter
	#print dijkstra algorithm stats
	print_stats(dijkstra, source_node_id, target_node_id, "D")

	A_star = dijkstra_Astar_SP(source_node_id, target_node_id, "A")		#call with A*("A") parameter
	#print A* algorithm stats
	print_stats(A_star, source_node_id, target_node_id, "A")


if __name__ == '__main__':
	main(sys.argv)