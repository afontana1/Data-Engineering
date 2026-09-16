#Apostolis Kasselouris, A.M:2994

#python version 3.8.5

import sys
import math
import heapq

network_list = []
#A position is of type [[node_x_axis, node_y_axis, neighbor_node_id, L2_distance, neighbor_node_id, L2_distance, ...]

global_visited_nodes = [] 	#contains the number of source nodes that have visited a node
global_max_SPD = []			#contains the max Shortest Path Distance(SPD) of source nodes from a node
#A node is in its corresponding position on the list eg node with id=5 is in network_list[5], global_max_SPD[5], etc position


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


#yields the next nearest neighbor node and its SPD of a node
def dijkstra_search(source):
	SPD = []		#Shortest Path Distance initialization for each node
	visited = []	#list that contains for each node if is visited or not(True or False type)
	#Important for above lists as well as with network_list the node is in the corresponding position of the lists
	#eg for node with id = 7 we can find if is visited with visited[7]. Same thing with all lists.
	#Also for SPD and path we store the shortest path and distance compared to source node(source compared to node_id)

	for node in network_list:
		SPD.append(math.inf)
		visited.append(False)

	#Shortest Path Distance from source(node) to source(node) is set to 0(obviously XD)
	SPD[source] = 0

	#Initialize and insert to priority queue a tuple of type (SPD, node_id)
	priority_queue = [(SPD[source], source)]
	priority_dict = {source : SPD[source]}	#initialize priority_dict for faster remove time in priority_queue
	
	while True:
		try:
			#get node_id with the shortest path distance 
			node_id = heapq.heappop(priority_queue)[1]
		except IndexError:
			#if IndexError priority_queue is empty this means a source node traversed through all nodes of the graph 
			#and we still haven't find a meeting node for the source nodes
			yield math.inf, -1	#return infinite SPD so as it is not choosed again from min()

		visited[node_id] = True

		yield SPD[node_id], node_id 

		for neighbor in neighbors(network_list[node_id]):
			neighbor_id = neighbor[0]
			weight = neighbor[1]	#L2 distance between node and its neighbor

			if not(visited[neighbor_id]):
				if(SPD[neighbor_id] > SPD[node_id] + weight):
					SPD[neighbor_id] = SPD[node_id] + weight
					
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


#returns the best meeting point for source nodes and the max SPD of source nodes from meeting node
def NRA(arg_list):
	global global_visited_nodes
	global global_max_SPD

	#initialize global_visited_nodes and global_max_SPD
	for node in network_list:
		global_visited_nodes.append(0)
		global_max_SPD.append(math.inf)

	source_node_generators = []	
	#contains the source nodes dijkstra object generator e.g
	#[dijkstra_search_object_generator_for_source_node_1, dijkstra_search_object_generator_for_source_node_2, ...]
	#dijkstra_search_object_generator yields a tuple containing (SPD[node_id], node_id)

	topK_list = [] #contains the last SPD and node_id where source nodes have visited through dijkstra e.g
	#[(SPD1, node_id1), (SPD2, node_id2), ...]
	#Important: A source node is in the same positions on the arg_list, source_node_generators and topK_list lists
	#eg a source node indexed in 4th position in arg_list is also in 4th position in source_node_generators and topK_list lists too

	priority_queue = [] #contains the last SPD and the index for the topK_list the SPD is refered to e.g
	#[(SPD, index_to_topK_list), (SPD, index_to_topK_list), ...]

	#Initialize source_node_generators, topK_list and priority queue
	for index, node in enumerate(arg_list):
		source_node_generators.append(dijkstra_search(node))	#append a dijstra generator for each source node
		topK_list.append(next(source_node_generators[-1]))		#append a tuple of type (SPD, node_id)
		priority_queue.append((topK_list[-1][0], index))		#append a tuple of type (SPD, index_to_topK_list)

	heapq.heapify(priority_queue)

	best_meeting_node_id = 0	#Initialize arbitrarily to 0 node

	while(True):
		min_tuple = heapq.heappop(priority_queue)	#get tuple (SPD, index of source node on topK_list)

		min_SPD = min_tuple[0]			#min SPD on topK_list
		index = min_tuple[1]			#index on topK_list that has min_SPD
		node_id = topK_list[index][1]	#node id that is on the specific index on topK_list

		#extreme case where source nodes are in unconnected graphs
		if min_SPD == math.inf:
			print("Error: No meeting node for source nodes found!")
			sys.exit(1)

		global_visited_nodes[node_id] += 1	

		#update global_max_SPD for a node
		if global_max_SPD[node_id] == math.inf:
			global_max_SPD[node_id] = min_SPD
		elif global_max_SPD[node_id] < min_SPD:
			global_max_SPD[node_id] = min_SPD
					
		#if node has been visited by all source nodes
		if(global_visited_nodes[node_id] == len(source_node_generators)):
			#if best_meeting_node has been visited by all nodes
			if global_visited_nodes[best_meeting_node_id] == len(source_node_generators):
				#If max SPD of the meeting node we found is smaller than the max SPD of the best meeting node
				#replace the best_meeting_node with the current meeting node
				if global_max_SPD[node_id] < global_max_SPD[best_meeting_node_id]:
					best_meeting_node_id = node_id
			#else initialize best_meeting_node_id with the first meeting node we found
			else:
				best_meeting_node_id = node_id
					
		#if min distance from topK_list is bigger than the current max SPD of the best meeting node
		#There is no possibility we find a better meeting node so we return
		if(min_SPD > global_max_SPD[best_meeting_node_id] and 
		global_visited_nodes[best_meeting_node_id] == len(source_node_generators)):
			return best_meeting_node_id, global_max_SPD[best_meeting_node_id]

		#update topK_list's source node with the next dijkstra SPD and node id
		topK_list[index] = next(source_node_generators[index])	
		#push to priority_queue(heap) a tuple of type (SPD topK_list[index] just got, index)
		heapq.heappush(priority_queue, (topK_list[index][0], index))
	

#checks the validity of the arguments and returns them as a list
def args_constructor(args):
	args.pop(0)	#remove topK_NRA.py
	args.pop(0)	#remove out.txt
	
	#extreme case where args have only on source node
	if(len(args) == 1):
		print("Best meeting node for source node", args[0], "is node", args[0])
		print("Max distance of source node", args[0], "from meeting node is", 0)
		sys.exit(0)

	arg_list = []
	for node in args:
		int_node = int(node)
		
		if not(int_node < 0 or int_node >= len(network_list)):
			arg_list.append(int_node)
		else:
			print("Error: Node with id", int_node, "not found!")
			print("Enter a number from 0 to", len(network_list)-1)
			sys.exit(1)

	return arg_list


def main(args):
	if not(len(args) > 2):
		print("Error: Wrong number of arguments.")
		print("Try: python3 topK_NRA.py out.txt node_id1 node_id2 ...")
		sys.exit(1)

	network = open(args[1], "r")
	
	#build the network_list
	build_network(network)

	#get the argument list containing node ids
	arg_list = args_constructor(args)

	#get the best meeting node for the argument lists nodes and their max SPD
	nra_stats = NRA(arg_list)

	#print stats
	print("Best meeting node for source nodes", arg_list, "is node:", nra_stats[0])
	print("Max shortest path distance =", nra_stats[1])


if __name__ == '__main__':
	main(sys.argv)