#Apostolis Kasselouris, A.M:2994

#python version 3.8.5

import csv
import sys

R_length = 0 #global variable for the length of R.tsv

#function that writes to the output file the last two lists of merge-sort algorithm removing duplicates and sum their values
def groupby_and_sum(left, right, output):
	i = j = sum = 0
	
	#while loop until we parse all the values of left or right list
	while(i < len(left) and j < len(right)):
		if(left[i][0] < right[j][0]): #if left list value is smaller than right list value
			if((i+1 < len(left)) and (left[i][0] == left[i+1][0])):	#if next row has duplicate first column to this row
				sum += left[i][1]
				i += 1
			else: #if next row is NOT duplicate to this row
				sum += left[i][1]
				output.writerow([left[i][0], sum])
				sum = 0 #reset sum
				i += 1
		elif(left[i][0] > right[j][0]): #if left list value is bigger than right list value
			if((j+1 < len(right)) and (right[j][0] == right[j+1][0])): #if next row has duplicate first column to this row
				sum += right[j][1]
				j += 1
			else: #if next row is NOT duplicate to this row
				sum += right[j][1]
				output.writerow([right[j][0], sum])
				sum = 0	#reset sum
				j += 1
		else: 							#if left list value is equal to right list value
			#if next row of left and right lists have duplicate first columns to this rows
			if((left[i][0] == left[i+1][0]) and (right[j][0] == right[j+1][0])):
				sum += left[i][1] + right[j][1]
				i += 1
				j += 1
			#if only the next row of left list has duplicate first column to this row
			elif((left[i][0] == left[i+1][0]) and (right[j][0] != right[j+1][0])):
				sum += left[i][1]
				i += 1
			#if only the next row of right list has duplicate first column to this row
			elif((left[i][0] != left[i+1][0]) and (right[j][0] == right[j+1][0])):
				sum += right[j][1]
				j += 1
			#if next row of left and right lists have NOT duplicate first columns to this rows
			else:
				sum += left[i][1] + right[j][1]
				output.writerow([left[i][0], sum]) #or right[j][0] its the same thing
				sum = 0 #reset sum
				i += 1
				j += 1

	#Checking if any element was left on left list
	while(i < len(left)):
		if((i+1 < len(left)) and (left[i][0] == left[i+1][0])):	#if next row has duplicate first column to this row
			sum += left[i][1]
			i += 1
		else: #if next row is NOT duplicate to this row
			sum += left[i][1]
			output.writerow([left[i][0], sum])
			sum = 0 #reset sum
			i += 1
		 
	#Checking if any element was left on right list
	while(j < len(right)):
		if((j+1 < len(right)) and (right[j][0] == right[j+1][0])): #if next row has duplicate first column to this row
			sum += right[j][1]
			j += 1
		else: #if next row is NOT duplicate to this row
			sum += right[j][1]
			output.writerow([right[j][0], sum])
			sum = 0	#reset sum
			j += 1


#merge-sort algorithm
def merge_sort(R, output):
	if(len(R) > 1):
		#Finding the mid of the array
		mid = len(R)//2

		#Dividing the R elements into 2 halves
		left = R[:mid]
		right = R[mid:]

		# Sorting the first half
		merge_sort(left, output)

		# Sorting the second half
		merge_sort(right, output)

		if(len(R) == R_length):	#if we are about to merge the last two lists go to groupby_and_sum function
			groupby_and_sum(left, right, output)
		else:
			i = j = k = 0
		
			# Copy data to temp arrays left[] and right[]
			while(i < len(left) and j < len(right)):
				if(left[i][0] < right[j][0]):
					R[k] = left[i]
					i += 1
				else:
					R[k] = right[j]
					j += 1
				k += 1

			# Checking if any element was left
			while(i < len(left)):
				R[k] = left[i]
				i += 1
				k += 1
		 
			while(j < len(right)):
				R[k] = right[j]
				j += 1
				k += 1


def main(args):
	global R_length

	if(len(args) != 2):
		print("Error: Wrong number of arguments")
		print("Try: python3 groupby.py R.tsv")
		sys.exit(1)

	R_fd = open(args[1], "r")	
	read_tsv = csv.reader(R_fd, delimiter="\t")

	#contains all the lines of the R.tsv file in a list
	R_list = []	#eg [['aa', 11], ['ab', 45], ...]
	#append rows of file in R_list whilst converting the second column of each row to integer
	for row in read_tsv:
  		R_list.append([row[0], int(row[1])])
	R_length = len(R_list) #set R_length

	with open('Rgroupby.tsv', 'w') as out_file:
		tsv_writer = csv.writer(out_file, delimiter='\t')

		#if R.tsv has only one row just ouput the row
		if(len(R_list) > 1):
			merge_sort(R_list, tsv_writer)	
		else:
			tsv_writer.writerow(R_row)
	
	R_fd.close()


main(sys.argv)