#Apostolis Kasselouris, A.M:2994

#python version 3.8.5

import sys

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
		lst.append(num)
	return lst


def construct_network(nodes, edges):
	#parse californias nodes file
	while(True):
		node = next_row(nodes)	#get next node

		if(len(node) > 1):
			node_x = float(node[1])	#x axis
			node_y = float(node[2])	#y axis

			network_list.append([node_x, node_y])
		else:
			nodes.close()	#close nodes file
			break


	#parse californias edges file
	while(True):
		edge = next_row(edges)	#get next edge

		if(len(edge) > 1):
			node_1 = int(edge[1])			#node 1
			node_2 = int(edge[2])			#connects with node 2
			L2_distance = float(edge[3])	#with Euclidean distance(L2)

			#add the edge between node 1 and node 2 to node 1 list
			network_list[node_1].append(node_2)
			network_list[node_1].append(L2_distance)

			#add the edge between node 1 and node 2 to node 2 list
			network_list[node_2].append(node_1)
			network_list[node_2].append(L2_distance)
		else:
			edges.close()	#close edges file
			break


#writes to out.txt file the network_list
def output_network(output):
	for id, node in enumerate(network_list):
		output.write(str(id) +' '+ ' '.join(map(repr, node)) + '\n')	#repr works almost the same as str


def main(args):
	if not(len(args) == 3):
		print("Error: Wrong number of arguments.")
		print("Try: python3 california_road_network.py cal.cnode.txt cal.cedge.txt")
		sys.exit(1)

	nodes = open(args[1], "r")	
	edges = open(args[2], "r")
	
	construct_network(nodes, edges)

	with open('out.txt', 'w') as out_file:
		#writes to out.txt file the network_list
		output_network(out_file)	


if __name__ == '__main__':
	main(sys.argv)