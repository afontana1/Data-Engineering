# Apostolis Kasselouris, A.M:2994

# python version 3.8.5

import sys
import json

R = [] #the R tree list

line_counter = 0		#number of line(query) we are counter
results_counter = 0		#number of results for a query counter
results_id = []			#the results for a query(MBRs ID that intersect query Window)


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


# return TRUE if querys window(W) and nodes MBR(node) intersect else return FALSE
def intersect(W, node):
	x_axis_intersect = False
	y_axis_intersect = False

	#check X-axis for possible intersection
	if(((node[1] >= W[0]) and (node[1] <= W[1])) or 
	((node[0] >= W[0]) and (node[0] <= W[1])) or 
	((node[0] <= W[0]) and (node[1] >= W[1]))):
		x_axis_intersect = True

	#check Y-axis for possible intersection
	if(((node[3] >= W[2]) and (node[3] <= W[3])) or 
	((node[2] >= W[2]) and (node[2] <= W[3])) or 
	((node[2] <= W[2]) and (node[3] >= W[3]))):
		y_axis_intersect = True

	#return
	if(x_axis_intersect and y_axis_intersect):
		return True
	else:
		return False


# change queries window form from
# [x-low, y-low, x-high, y-high] to [x-low, x-high, y-low, y-high]
def normalize_query(query):
	# if list not empty
	if(len(query) > 1):
		temp = query[1]
		query[1] = query[2]
		query[2] = temp

	return query


def range_queries(query, node):
	global results_counter
	global results_id

	if(node[0] == 1):	#non-leaf node
		for entry in node[2]:
			if(intersect(query, entry[1])):
				range_queries(query, R[entry[0]])
	else:				#leaf node
		for entry in node[2]:
			if(intersect(query, entry[1])):
				results_id.append(entry[0])
				results_counter+=1


def build_Rtree(Rtree):
	global R
	Rtree_raw = Rtree.readlines()

	for node in Rtree_raw:
		# convert a node from a string to a list
		R.append(json.loads(node))
	Rtree_raw.clear()


def main(args):
	global line_counter
	global results_counter
	global results_id

	if not(len(args) == 3):
		print("Error: Wrong number of arguments.")
		print("Try: python3 range_queries.py Rtree.txt Rqueries.txt")
		sys.exit(1)

	Rtree = open(args[1], "r")
	Rqueries = open(args[2], "r")

	#build the R tree list
	build_Rtree(Rtree)
	
	#parse queries
	query = normalize_query(next_row(Rqueries))
	while(len(query) > 1):
		range_queries(query, R[-1])	#(query, root node)
		query = normalize_query(next_row(Rqueries))

		#print results
		print(str(line_counter) +" ("+str(results_counter)+"): "+ ', '.join(map(str, results_id)))

		#set for next query
		line_counter += 1
		results_counter = 0
		results_id.clear()

	Rtree.close()
	Rqueries.close()


if __name__ == '__main__':
	main(sys.argv)