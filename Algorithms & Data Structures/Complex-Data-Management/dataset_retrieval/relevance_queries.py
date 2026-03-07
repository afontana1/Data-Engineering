#Apostolis Kasselouris, A.M:2994

#python version 3.8.5

import sys
import time
import json
import heapq
import math


K = 0	#K most relevant results user wants

#global list containing all transaction sets
transactions = []	#eg transactions = [{5, 8, 3, 1}, {...}, ...]
					#{5, 8, 3 , 1} is a single transaction set

inverted_list = []	#contains for each item its inverted list (of transactions)

inverted_occ_list = []	#contains transactions that include an item plus its occurences in that transaction for all items
						#eg [[transaction_that_includes_item0, item0_occurrence_in_that_transaction], [...], ...]

T_trf_list = []		#of type [|T|/trf(0,T), |T|/trf(1,T), ..., |T|/trf(243,T)] (for all items)
					#eg [total_transactions / in_how_many_transactions_does_item43_exists, ...]

#method transaction results (used only for single query)
naive_results = []
inverted_file_results = []

#timers
naive_timer = 0
inverted_file_timer = 0


#parses and yields transactions and its occurrences for an item list in inverted_occ_list
def list_parser(lst):
	for i in lst:
		yield i

	#when end of list reached yield [math.inf, -1] list whenever called
	while(1):
		yield [math.inf, -1]
		

def create_inverted_list():
	global inverted_list

	#find max id of items in all transactions
	max_item = max(transactions[0])
	for transaction in transactions:
		temp_max_item = max(transaction)
		if(max_item < temp_max_item):
			max_item = temp_max_item
		
	for item in range(max_item + 1):	#for each available item
		item_in_transactions = []	#STORES the transactions that contain the corresponding item

		#FIND the transactions that contain the corresponding item
		for id, transaction in enumerate(transactions):
			if(item in transaction):
				item_in_transactions.append(id)

		inverted_list.append(sorted(item_in_transactions))	#store the transactions sorted


def create_inverted_file_occurence():
	global inverted_occ_list
	global T_trf_list

	T = len(transactions)	#total transactions
		
	#T_trf_list creation
	for item_list in inverted_list:
		try:
			T_trf_list.append(T / len(item_list))
		except ZeroDivisionError:
			T_trf_list.append(0)

	#inverted_occ_list creation
	with open('invfileocc.txt', 'w') as output:
		for item, item_list in enumerate(inverted_list):
			item_occurrence_list = []	#STORES an items transactions and its occurrences in that transaction
										#eg for item3 [[transaction_that_includes_it, items_occurrence_in_that_transaction], [...], ...]

			for transaction_id in item_list:
				item_occurrence_list.append([transaction_id, transactions[transaction_id].count(item)])

			#append and write
			inverted_occ_list.append(item_occurrence_list)
			output.write(str(item)+": "+ str(T_trf_list[item]) +", "+ str(inverted_occ_list[-1]) +"\n")
		

def naive_method(query):
	global naive_results

	rel = []	#list that contains the rel(t, q) and id of a transaction
				#eg [[rel55, 55], [rel3, 3], ...]

	for id, transaction in enumerate(transactions):
		transaction_rel = 0

		for item in query:
			transaction_rel += transactions[id].count(item) * T_trf_list[item]	#rel(t,q) = SUM(i E q) (occ(i,t) * |T|/trf(i,T))

		if(transaction_rel > 0):
			rel.append([transaction_rel, id])

	naive_results = heapq.nlargest(K, rel)	#give to naive_results the K largest transactions relations to query in descending order


def inverted_file_method(query):
	global inverted_file_results

	rel = []	#list that contains the rel(t, q) and id of a transaction
				#eg [[rel55, 55], [rel3, 3], ...]

	item_generators = []	#contains the generators for inverted_list of an item
							#eg [query_item55_generator, query_item3_generator, ...]
	item_transactions = []	#contains a tuple of type (the current transaction we are on the inverted_list for an item, item)
							#eg [([inverted_list_next_transaction_for_query_item55, occurrence_of_item55_in_transaction], query_item55_index_on_item_generators), 
							# 		([inverted_list_next_transaction_for_query_item3, occurrence_of_item55_in_transaction], query_item3_index_on_item_generators), ...]
	
	#initialize above lists
	for index, item in enumerate(query):
		item_generators.append(list_parser(inverted_occ_list[item]))
		item_transactions.append((next(item_generators[-1]), index))

	while(True):
		min_tuple = item_transactions[0]	#of type ([transaction, occurence], index_on_item_generators)

		#find min element on item_transactions
		for it in item_transactions[1:]:	#parse item_transactions list EXCEPT first element
			if(it[0][0] < min_tuple[0][0]):
				min_tuple = it

		#if ALL lists are fully parsed break
		if(min_tuple[0][0] == math.inf):
			break

		min_transaction = min_tuple[0][0]
		min_index = min_tuple[1]	#index for item_generators and query elements

		#calculate a transaction relation to a querys item
		occ = item_transactions[min_index][0][1]
		T_trf = T_trf_list[query[min_index]]
		transaction_rel = occ * T_trf

		try:
			if(rel[-1][1] != min_transaction):	#new transaction
				rel.append([transaction_rel, min_transaction])
			else:	#append to an already existing transaction 
				rel[-1][0] += transaction_rel
		except IndexError:	#only if len(rel) == 0 (1 time only case)
			rel.append([transaction_rel, min_transaction])

		item_transactions[min_index] = (next(item_generators[min_index]), item_transactions[min_index][1])	#move to next transaction for an item
	
	inverted_file_results = heapq.nlargest(K, rel)	#give to inverted_file_results the K largest transactions relations to query in descending order


def print_results(query_line, method):
	if(method == -1):	#all methods
		if(query_line == -1):	#all queries
			print("Naive Method computation time =", naive_timer)
			print("Inverted File Computation time =", inverted_file_timer)
		else:	#specific query
			print("Naive method results:")
			print(naive_results)
			print("Naive Method computation time =", naive_timer)

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
	elif(method == 1):	#inverted file method
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
	global inverted_file_timer
	global K

	if not(len(args) == 6):
		print("Error: Wrong number of arguments.")
		print("Try: python3 containment_queries.py transactions.txt queries.txt <query_number> <method> <k_most_relevant_results>")
		sys.exit(1)

	query_line = int(args[3])	#query line we want to use(if -1 use all queries)
	method = int(args[4])	#-1: all methods
							# 0: naive method
							# 1: exact signature file method
							# 2: exact bitslice signature file method 
							# 3: inverted file method
	K = int(args[5])	#K most relevant results

	#load transactions
	with open(args[1]) as transactions_file:
		for line in transactions_file:
			transactions.append(json.loads(line))	#append transactions as lists

	create_inverted_list()
	create_inverted_file_occurence()

	#parse queries
	with open(args[2]) as queries_file:
		for line_num, line in enumerate(queries_file):
			if(line_num == query_line or query_line == -1):
				query = json.loads(line)	#get query list
				
				if(method == -1):	#all methods
					start_time = time.time()
					naive_method(query)
					end_time = time.time()
					naive_timer += end_time - start_time

					start_time = time.time()
					inverted_file_method(query)
					end_time = time.time()
					inverted_file_timer += end_time - start_time
				elif(method == 0):	#naive method
					start_time = time.time()
					naive_method(query)
					end_time = time.time()
					naive_timer += end_time - start_time
				elif(method == 1):	#inverted file method
					start_time = time.time()
					inverted_file_method(query)
					end_time = time.time()
					inverted_file_timer += end_time - start_time
				else:
					print("Error: Method "+ str(method) +"does not exists!")

	print_results(query_line, method)
	

if __name__ == '__main__':
	main(sys.argv)