#Apostolis Kasselouris, A.M:2994

#python version 3.8.5

import sys
import time
import json
import math


#global list containing all transaction sets
transactions = []	#eg transactions = [{5, 8, 3, 1}, {...}, ...]
					#{5, 8, 3 , 1} is a single transaction set

sigfile = []		#contains the signatures for each transaction
bitslice = []		#contains the bitslice signatures for each transaction

inverted_list = []	#contains for each item its inverted list (of transactions)

#method transaction results (used only for single query)
naive_results = set()
exact_signature_file_results = set()
exact_bitslice_signature_file_results = set()
inverted_file_results = set()

#timers
naive_timer = 0
exact_signature_file_timer = 0
exact_bitslice_signature_file_timer = 0
inverted_file_timer = 0


#parses and yields transactions for an item list in inverted_list
#FOR 3rd solution on inverted file method
def list_parser(lst):
	for i in lst:
		yield i

	#when end of list reached yield -1 whenever called
	while(1):
		yield -1	


#takes 2 sorted lists and returns their intersection list
#FOR 2nd solution on inverted file method
def intersection_merge(list1, list2):
	list1_len = len(list1)
	list2_len = len(list2)

	index1 = 0
	index2 = 0
	intersection_list = []

	while(index1 < list1_len and index2 < list2_len):
		if(list1[index1] < list2[index2]):
			index1 += 1
		elif(list1[index1] > list2[index2]):
			index2 += 1
		else:
			intersection_list.append(list1[index1])
			index1 += 1
			index2 += 1

	return intersection_list


def create_transactions_signature():
	global sigfile

	with open('sigfile.txt', 'w') as out_file:
		for transaction in transactions:
			bitmap = 0
			
			#create signature(bitmap) for a transaction
			for item in transaction:
				bitmap += 2**item

			#append and write
			sigfile.append(bitmap)	
			out_file.write(str(bitmap) + "\n")	

def bitmap_query(query):
	bitmap = 0
	for item in query:
		bitmap += 2**item

	return bitmap
		

def create_transactions_bitslice_signature_and_inverted_file():
	global bitslice
	global inverted_list

	#find max id of items in all transactions
	max_item = max(transactions[0])
	for transaction in transactions:
		temp_max_item = max(transaction)
		if(max_item < temp_max_item):
			max_item = temp_max_item
		
	#create bitslice map for all items
	with open('bitslice.txt', 'w') as bitslice_file, open('invfile.txt', 'w') as inverted_file:
		for item in range(max_item + 1):	#for each available item
			item_in_transactions = []	#STORES the transactions that contain the corresponding item

			#FIND the transactions that contain the corresponding item
			for id, transaction in enumerate(transactions):
				if(item in transaction):
					item_in_transactions.append(id)
			
			#calculate the bitslice for an item
			item_bitslice = 0
			for transaction_id in item_in_transactions:
				item_bitslice += 2**transaction_id

			#append and write for bitslice signature
			bitslice.append(item_bitslice)
			bitslice_file.write(str(item)+": "+ str(item_bitslice) +"\n")	

			#append and write for inverted file
			inverted_list.append(sorted(item_in_transactions))	#store the transactions sorted
			inverted_file.write(str(item)+": "+ str(inverted_list[-1]) +"\n")	
		

def naive_method(query):
	global naive_results

	for id, transaction in enumerate(transactions):
		if(query.issubset(transaction)):
			naive_results.add(id)


def exact_signature_file_method(query):
	global exact_signature_file_results

	sig_query = bitmap_query(query)

	for transaction_id, signature in enumerate(sigfile):
		if((signature & sig_query) == sig_query):	#bitwise AND operation between a transactions signature and a querys signature
			exact_signature_file_results.add(transaction_id)


def exact_bitslice_signature_file_method(query):
	global exact_bitslice_signature_file_results

	#bitwise AND operation between each item of querys bitslice
	flag = True
	for item in query:
		if(flag):
			bitmap = bitslice[item]
			flag = False
		
		bitmap &= bitslice[item]
	
	#each position of a bit on bitmap is a transaction id
	for transaction_id, bit in enumerate(bin(bitmap)[::-1]):
	#[::-1] is a type of extended slicing: 
	#::-1 means we parse the bitmap binary string in reverse order from left to right(least to most significant bit)
		if(bit == '1'):
			exact_bitslice_signature_file_results.add(transaction_id)


def inverted_file_method(query):
	global inverted_file_results

	#1st solution
	#use of set intersection to merge join query items inverted lists
	#(Extremely fast solution due to intersection() being precompiled)
	'''results = []
	for item in query:
		results.append(set(inverted_list[item]))

	inverted_file_results = results[0].intersection(*results)'''

	#2nd solution
	#Intersect two lists at a time and then take the resulted list and intersect it with the 3rd list and so on at there are no lists left
	#(This solution is almost as fast as the bitslice signature file method)
	'''if(len(query) == 1):
		inverted_file_results = set(inverted_list[next(iter(query))])
		return

	counter = 0
	for item in query:
		if(counter == 0):
			first_item = item
			counter += 1
		elif(counter == 1):
			intersected_list = intersection_merge(inverted_list[first_item], inverted_list[item])
			counter += 1
		else:
			intersected_list = intersection_merge(intersected_list, inverted_list[item])


	inverted_file_results = set(intersected_list)'''


	#3rd solution
	#Multi-way intersection
	#This is by far the slowest solution of them all because of the interpreted nature of python
	#If we would run this code in a compiled language this would be the fastest solution 
	item_generators = []	#contains the generators for inverted_list of an item
							#eg [query_item55_generator, query_item3_generator, ...]
	item_transactions = []	#contains a tuple of type (the current transaction we are on the inverted_list for an item, item)
							#eg [(inverted_list_next_transaction_for_query_item55, query_item55_index_on_item_generators), 
							# 		(inverted_list_next_transaction_for_query_item3, query_item3_index_on_item_generators), ...]

	#initialize above lists
	for index, item in enumerate(query):
		item_generators.append(list_parser(inverted_list[item]))
		item_transactions.append((next(item_generators[-1]), index))


	while(True):
		min_tuple = item_transactions[0]
		previous_transaction = min_tuple[0]
		equality_flag = True	#True only if a transaction is common on all item_transactions(aka if True intersect)

		#find min element on item_transactions and equality_flag
		for it in item_transactions[1:]:	#parse item_transactions list EXCEPT first element
			if(it[0] < min_tuple[0]):
				min_tuple = it

			if not(previous_transaction == it[0]):
				equality_flag = False

		#if ANY list is fully parsed break
		if(min_tuple[0] == -1):
			break

		min_transaction = min_tuple[0]
		min_index = min_tuple[1]

		if(equality_flag):	#intersect
			inverted_file_results.add(min_transaction)	#add to results min_transaction

			#move to next transaction for all items
			for index, item_generator in enumerate(item_generators):
				item_transactions[index] = (next(item_generator), item_transactions[index][1])
		else:	#move to next transaction for min item
			item_transactions[min_index] = (next(item_generators[min_index]), item_transactions[min_index][1])
	


def print_results(query_line, method):
	if(method == -1):	#all methods
		if(query_line == -1):	#all queries
			print("Naive Method computation time =", naive_timer)
			print("Signature File computation time =", exact_signature_file_timer)
			print("Bitsliced Signature File computation time =", exact_bitslice_signature_file_timer)
			print("Inverted File Computation time =", inverted_file_timer)
		else:	#specific query
			print("Naive method results:")
			print(naive_results)
			print("Naive Method computation time =", naive_timer)

			print(" ")

			print("Signature File result:")
			print(exact_signature_file_results)
			print("Signature File computation time =", exact_signature_file_timer)

			print(" ")

			print("Bitsliced Signature File result:")
			print(exact_bitslice_signature_file_results)
			print("Bitsliced Signature File computation time =", exact_bitslice_signature_file_timer)

			print(" ")

			print("Inverted File result:")
			print(inverted_file_results)
			print("Inverted File Computation time =", inverted_file_timer)
	elif(method == 0):	#naive method
		if(query_line == -1):	#all queries
			print("Naive Method computation time =", naive_timer)
		else:	#specific query
			print("Naive method results:")
			print(naive_results)
			print("Naive Method computation time =", naive_timer)
	elif(method == 1):	#exact signature file method
		if(query_line == -1):	#all queries
			print("Signature File computation time =", exact_signature_file_timer)
		else:	#specific query
			print("Signature File result:")
			print(exact_signature_file_results)
			print("Signature File computation time =", exact_signature_file_timer)
	elif(method == 2):	#exact bitslice signature file method 
		if(query_line == -1):	#all queries
			print("Bitsliced Signature File computation time =", exact_bitslice_signature_file_timer)
		else:	#specific query
			print("Bitsliced Signature File result:")
			print(exact_bitslice_signature_file_results)
			print("Bitsliced Signature File computation time =", exact_bitslice_signature_file_timer)
	elif(method == 3):	#inverted file method
		if(query_line == -1):	#all queries
			print("Inverted File Computation time =", inverted_file_timer)
		else:	#specific query
			print("Inverted File result:")
			print(inverted_file_results)
			print("Inverted File Computation time =", inverted_file_timer)
	else:
		print("Error: Method "+ str(method) +"does not exists!")
		sys.exit(1)


def main(args):
	global naive_timer
	global exact_signature_file_timer
	global exact_bitslice_signature_file_timer
	global inverted_file_timer

	if not(len(args) == 5):
		print("Error: Wrong number of arguments.")
		print("Try: python3 containment_queries.py transactions.txt queries.txt <query_number> <method>")
		sys.exit(1)

	query_line = int(args[3])	#query line we want to use(if -1 use all queries)
	method = int(args[4])	#-1: all methods
							# 0: naive method
							# 1: exact signature file method
							# 2: exact bitslice signature file method 
							# 3: inverted file method

	#load transactions
	with open(args[1]) as transactions_file:
		for line in transactions_file:
			transactions.append(set(json.loads(line)))	#append transactions as sets

	create_transactions_signature()
	create_transactions_bitslice_signature_and_inverted_file()

	#parse queries
	with open(args[2]) as queries_file:
		for line_num, line in enumerate(queries_file):
			if(line_num == query_line or query_line == -1):
				query = set(json.loads(line))	#get query set
				
				if(method == -1):	#all methods
					start_time = time.time()
					naive_method(query)
					end_time = time.time()
					naive_timer += end_time - start_time

					start_time = time.time()
					exact_signature_file_method(query)
					end_time = time.time()
					exact_signature_file_timer += end_time - start_time

					start_time = time.time()
					exact_bitslice_signature_file_method(query)
					end_time = time.time()
					exact_bitslice_signature_file_timer += end_time - start_time

					start_time = time.time()
					inverted_file_method(query)
					end_time = time.time()
					inverted_file_timer += end_time - start_time
				elif(method == 0):	#naive method
					start_time = time.time()
					naive_method(query)
					end_time = time.time()
					naive_timer += end_time - start_time
				elif(method == 1):	#exact signature file method
					start_time = time.time()
					exact_signature_file_method(query)
					end_time = time.time()
					exact_signature_file_timer += end_time - start_time
				elif(method == 2):	#exact bitslice signature file method 
					start_time = time.time()
					exact_bitslice_signature_file_method(query)
					end_time = time.time()
					exact_bitslice_signature_file_timer += end_time - start_time
				elif(method == 3):	#inverted file method
					start_time = time.time()
					inverted_file_method(query)
					end_time = time.time()
					inverted_file_timer += end_time - start_time
				else:
					print("Error: Method "+ str(method) +"does not exists!")

	print_results(query_line, method)
	

if __name__ == '__main__':
	main(sys.argv)