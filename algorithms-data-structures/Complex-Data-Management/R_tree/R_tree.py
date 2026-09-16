#Apostolis Kasselouris, A.M:2994

#python version 3.8.5

import sys
import math

NODE_MAX_CAPACITY = 0
NODE_MIN_CAPACITY = 0

nodes_counter = 0	#counts the number of total nodes in R tree
level_counter = 0	#counts the number of levels in R tree


#yields lines of a file as objects
def parser(fname):
	for line in fname.readline().strip().split(','):
		yield line

#returns next lines values of a file as a list
def next_row(fd):
	line_obj = parser(fd)
	lst = []
	for num in line_obj:
		lst.append(num)
	return lst


#interleave_latlng function taken from https://github.com/trevorprater/pymorton/blob/master/pymorton/pymorton.py
#returns a Z-order type integer for the center point of an MBR
def interleave_latlng(lat, lng):
	_DIVISORS = [180.0 / 2 ** n for n in range(32)]

	if not isinstance(lat, float) or not isinstance(lng, float):
		print('Usage: interleave_latlng(float, float)')
		raise ValueError("Supplied arguments must be of type float!")

	if (lng > 180):
		x = (lng % 180) + 180.0
	elif (lng < -180):
		x = (-((-lng) % 180)) + 180.0
	else:
		x = lng + 180.0
	if (lat > 90):
		y = (lat % 90) + 90.0
	elif (lat < -90):
		y = (-((-lat) % 90)) + 90.0
	else:
		y = lat + 90.0

	morton_code = ""
	for dx in _DIVISORS:
		digit = 0
		if (y >= dx):
			digit |= 2
			y -= dx
		if (x >= dx):
			digit |= 1
			x -= dx
		morton_code += str(digit)

	return morton_code


#calculate MBR(Minimum Bounding Rectangle) for an object
def calculate_MBR(object_coords_list):
	x_axis_list = []
	y_axis_list = []
	for point in object_coords_list:
		x_axis_list.append(point[0])
		y_axis_list.append(point[1])

	#return MBR in this form [x-low, x-high, y-low, y-high]
	return [min(x_axis_list), max(x_axis_list), min(y_axis_list), max(y_axis_list)]
	
	
#calculate the MBR of a non leaf node using previous nodes
def calculate_non_leaf_MBR(row):
	id = row[1]	#the ID of the previous node we point

	#calculate MBR of MBRs
	x_low_list = []
	x_high_list = []
	y_low_list = []
	y_high_list = []

	for mbr in row[2]:
		x_low_list.append(mbr[1][0])
		x_high_list.append(mbr[1][1])
		y_low_list.append(mbr[1][2])
		y_high_list.append(mbr[1][3])
	
	x_low = min(x_low_list)
	x_high = max(x_high_list)
	y_low = min(y_low_list)
	y_high = max(y_high_list)
	x_low_list.clear()
	x_high_list.clear()
	y_low_list.clear()
	y_high_list.clear()

	return [id, [x_low, x_high, y_low, y_high]]


#returns a level of the R tree
def level_constructor(mbr, is_non_leaf):
	global nodes_counter

	level_list = []		#contains the nodes of a level
	node_list = []		#contains the MBRs of a node

	for num, row in enumerate(mbr):
		if(is_non_leaf):	#non leaf
			node_list.append(calculate_non_leaf_MBR(row))
		else:				#leaf
			node_list.append(row[1])	#append and MBR and its ID on a node

		if(num % NODE_MAX_CAPACITY == NODE_MAX_CAPACITY-1):
			level_list.append([is_non_leaf, nodes_counter, node_list])
			nodes_counter+=1
			node_list = []	#reset list to load MBRs of next node
	
	#LAST NODE CASES
	#no extra last node case
	if(len(node_list) == 0):
		return level_list
	#last node meets minimum MBR criteria
	elif(len(node_list) >= NODE_MIN_CAPACITY):
		level_list.append([is_non_leaf, nodes_counter, node_list])	#create last node
		nodes_counter+=1
	#last node is too small and must be filled with MBRs from previous node
	else:
		#while last node is smaller than minimum fill it with previous nodes MBRs
		while(len(node_list) < NODE_MIN_CAPACITY):
			poped_MBR = level_list[-1][2].pop()
			node_list.insert(0, poped_MBR)

		level_list.append([is_non_leaf, nodes_counter, node_list])	#create last node
		nodes_counter+=1

	return level_list	#return level


#returns the leaves list of the R tree
def leaves_constructor(coords, offsets):
	offset = next_row(offsets)	
	object_coords_list = []	#initialize a list that stores the coordinates for each edge of an object
	MBR_list = []	#initialize a list that stores the MBR_with_ID's of all object and their z_int

	#parse offsets file
	while(len(offset) > 1):
		#get an objects coordinates from coords file
		for i in range(int(offset[1]), int(offset[2])+1):
			point = next_row(coords)
			if not(len(point) > 1):
				print("Error: coords.txt reached EOF while offsets.txt was still running!")
				sys.exit(1)
			object_coords_list.append(list(map(float, point)))
			
		MBR = calculate_MBR(object_coords_list)	#calculate MBR for an object
		object_coords_list.clear()	#clear list

		#get the Z-order integer for the center point of an MBR
		Z_int = interleave_latlng((MBR[2]+MBR[3])/2, (MBR[0]+MBR[1])/2) #(y, x)

		MBR_with_ID = [int(offset[0]), MBR]	#[id, MBR] e.g [5, [1.2, 2.1, 3.8, 4.3]]

		MBR_list.append([Z_int, MBR_with_ID])	#e.g [3413754436..., [5, [1.2, 2.1, 3.8, 4.3]]]

		offset = next_row(offsets)	#next objects id and offset values

	#order MBR_list based on Z_int
	sorted_MBR_list = sorted(MBR_list, key=lambda x:x[0])

	coords.close()
	offsets.close()

	#return the leaves list of the R tree
	return level_constructor(sorted_MBR_list, 0)


#returns the root level of the R tree
def root_constructor(mbr, is_non_leaf):
	level_list = []		#contains the nodes of a level
	node_list = []		#contains the MBRs of a node

	for row in mbr:
		node_list.append(calculate_non_leaf_MBR(row))

	level_list.append([is_non_leaf, nodes_counter, node_list])

	return level_list


#create the R tree
def R_tree(level_nodes, output):
	global level_counter

	#print statistics about R tree
	print(len(level_nodes), "nodes at level", level_counter)
	level_counter += 1

	#write level of the R tree to Rtree.txt
	for node in level_nodes:
		output.write(str(node) + '\n')

	if(len(level_nodes) > NODE_MAX_CAPACITY):	#non-root level
		non_leaf_level = level_constructor(level_nodes, 1)

		#recursively call R_tree() to build the R tree from leaves to root
		R_tree(non_leaf_level, output)	
	else:										#root level
		root_level = root_constructor(level_nodes, 1)

		#print statistics about R tree
		print(len(root_level), "nodes at level", level_counter)

		#write root level of the R tree to Rtree.txt
		for node in root_level:
			output.write(str(node))


def main(args):
	global NODE_MAX_CAPACITY
	global NODE_MIN_CAPACITY

	if not(len(args) == 4):
		print("Error: Wrong number of arguments.")
		print("Try: python3 R_tree.py coords.txt offsets.txt node_size(eg. 20)")
		sys.exit(1)

	coords = open(args[1], "r")	
	offsets = open(args[2], "r")
	NODE_MAX_CAPACITY = int(args[3])						#set nodes max capacity of MBRs
	NODE_MIN_CAPACITY = math.ceil(NODE_MAX_CAPACITY * 0.4)	#set nodes min capacity of MBRs

	#get the leaves list of the R tree
	leaves_list = leaves_constructor(coords, offsets)

	with open('Rtree.txt', 'w') as out_file:
		#create the R tree
		R_tree(leaves_list, out_file)


if __name__ == '__main__':
	main(sys.argv)