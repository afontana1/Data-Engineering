#Apostolis Kasselouris, A.M:2994

#python version 3.8.5

import csv
import sys

#constants
BIG_NUM = 99999999
BIG_CHAR = '~~'

max_buffer = 0 #holds the max size buffer list reached at one point of time

R_EOF = False	#True if we reach EOF on R_sorted file
S_EOF = False	#True if we reach EOF on S_sorted file

#list we return if we reach EOF
#if one column of the input files is string the actual value we return is BIG_CHAR instead of BIG_NUM
EOF_list = [BIG_NUM, BIG_NUM]	

#yields lines of a file as objects
def parser(fname):
	for line in fname.readline().strip():
		line = line.split('\t')
		yield line

#return correct form of readline eg from [['a'],['', ''], ['b']] to ['a','b']
def correct_form(lst):
	global EOF_list

	flag = True
	col1 = []
	col2 = []

	for char in lst:
		if(len(char) == 2):
			flag = False
			continue
		if(flag):
			col1.append(char[0])
		else:
			col2.append(char[0])

	#if string is actually integer convert it to integer or else leave it as string
	try:
		val1 = int("".join(col1))
	except ValueError:
		val1 = "".join(col1)
		EOF_list[0] = BIG_CHAR	#change EOF_list[0] so as to be compared with strings

	try:
		val2 = int("".join(col2))
	except ValueError:
		val2 = "".join(col2)
		EOF_list[1] = BIG_CHAR	#change EOF_list[1] so as to be compared with strings

	return [val1, val2] #eg ['aa', 11]

#returns next lines values of a file as a list
def next_row(fd):
	line_obj = parser(fd)
	lst = []
	for char in line_obj:
		lst.append(char)

	#check for EOF and return an array with characters with ASCII numbers higher than any english character ASCII number
	#or if we compare integers return an integer that is way higher than any integer on the file
	if len(lst) == 0:
		return EOF_list

	return correct_form(lst)


def check_for_EOF_R(R_row):
	global R_EOF
	
	if((R_row[0] == BIG_CHAR) or (R_row[0] == BIG_NUM)):
		R_EOF = True

def check_for_EOF_S(S_row):
	global S_EOF

	if((S_row[0] == BIG_CHAR) or (S_row[0] == BIG_NUM)):
		S_EOF = True

def check_for_empty_files(R_row, S_row):
	if((R_row[0] == BIG_CHAR) and (S_row[0] == BIG_CHAR) or (R_row[0] == BIG_NUM) and (S_row[0] == BIG_NUM)):
		print("Can't merge two empty files")
		sys.exit(0)
	elif((R_row[0] == BIG_CHAR) or (R_row[0] == BIG_NUM)):
		print("R_sorted file is empty. Merge not completed")
		sys.exit(0)
	elif((S_row[0] == BIG_CHAR) or (S_row[0] == BIG_NUM)):
		print("S_sorted file is empty. Merge not completed")
		sys.exit(0)


#if R has duplicate values in its first column output them too
def check_for_duplicates(output, buffer, R_row):
	global max_buffer

	if(len(buffer) != 0):
		if(buffer[0][0] == R_row[0]):
			for buf in buffer:
				output.writerow(R_row + [buf[1]])
		else:
			#reevaluate max_buffer before clearing the buffer
			if(len(buffer) > max_buffer):
				max_buffer = len(buffer)

			buffer.clear()


def merge_join(R, S, output):
	#get the first row of each file
	R_row = next_row(R)
	S_row = next_row(S)

	buffer = [] #buffer for S_sorted file rows in case of duplicate values of R_sorted

	check_for_empty_files(R_row, S_row)

	while True:
		#IMPORTANT! If we reach EOF on both files we break the while-loop
		if(R_EOF and S_EOF):
			break

		if(R_row[0] == S_row[0]):
			output.writerow(R_row + [S_row[1]])
			
			buffer.append(S_row)
			S_row = next_row(S)
			check_for_EOF_S(S_row)
		elif(R_row[0] < S_row[0]):
			R_row = next_row(R)
			check_for_EOF_R(R_row)

			check_for_duplicates(output, buffer, R_row)
		elif(R_row[0] > S_row[0]):
			S_row = next_row(S)
			check_for_EOF_S(S_row)


def main(args):
	if(len(args) != 3):
		print("Error: Wrong number of arguments")
		print("Try: python3 merge_join.py R_sorted.tsv S_sorted.tsv")
		sys.exit(1)

	R_sorted_fd = open(args[1], "r")	
	S_sorted_fd = open(args[2], "r")

	with open('RjoinS.tsv', 'w') as out_file:
		tsv_writer = csv.writer(out_file, delimiter='\t')

		merge_join(R_sorted_fd, S_sorted_fd, tsv_writer)

	print("Max size(length) buffer list reached was:", max_buffer)

	R_sorted_fd.close()
	S_sorted_fd.close()
			

main(sys.argv)