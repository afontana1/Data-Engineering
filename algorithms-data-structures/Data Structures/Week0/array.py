

class ArrayMethods:
	def __init__(self):
		pass

	def array_advance(self,A):
		'''
		objective is to get to the end of the array
		in as little moves as possible
		you are constrained by the numbers in the index positions
		'''
		furthest_reached = 0
		last_idx = len(A) - 1
		i = 0
		while i <= furthest_reached and furthest_reached < last_idx:
			furthest_reached = max(furthest_reached, A[i] + i)
			i += 1
		return furthest_reached >= last_idx
	
	def two_sum(self,array,target):
		for i in range(len(array)-1):
			for j in range(i+1,len(array)):
				if (array[i] + array[j]) == target:
					return True
		return False

	def two_sum_LinearTime(self,array,target):
		memory = {}
		for i in range(len(array)):
			if array[i] in memory:
				return True
			else:
				memory[target-array[i]] = array[i]
		return False

	def intersection(self,arr1,arr2):
		'''intersection of two sorted arrays'''
		common = []
		i,j = 0,0
		while (i < len(arr1)) and (j < len(arr2)):
			element1,element2 = arr1[i] , arr2[j]
			if element1 < element2:
				i+=1
			elif element1 > element2:
				j+=1
			else:
				if element1 not in common:
					common.append(element1)
				i+=1
				j+=1
		return common

	def complement(self,arr1,arr2):
		'''complement of two sorted arrays'''
		intersect = self.intersection(arr1,arr2)
		if not intersect:
			return []
		while intersect:
			element = intersect.pop(0)
			while True:
				if element in arr1:
					arr1.pop(arr1.index(element))
				elif element in arr2:
					arr2.pop(arr2.index(element))
				else:
					break
		return arr1 + arr2

	def union(self,arr1,arr2):
		'''union of two sorted arrays'''
		comp = self.complement(arr1,arr2)
		if not comp:
			return []
		inter = self.intersection(arr1,arr2)
		return comp + inter

	def difference(self,arr1,arr2):
		'''difference of two sorted arrays'''
		diff = []
		for i in range(len(arr1)):
			if arr1[i] not in arr2:
				if arr1[i] not in diff:
					diff.append(arr1[i])
		return diff

	def intersection_unsorted(self,arr1,arr2):
		smaller = arr1
		larger = arr2
		intersect = []
		i = 0
		if len(arr1)>len(arr2):
			smaller = arr2
			larger = arr1
		while i < len(smaller):
			element = smaller[i]
			if element in larger and element not in intersect:
				intersect.append(element)
			i+=1
		return intersect

	def stock_price(self,stock_prices):
		profit = 0
		while stock_prices:
			cheapest = min(stock_prices)
			position_of_cheapest = stock_prices.index(cheapest)
			actual_element = stock_prices[position_of_cheapest]
			subset_of_prices = stock_prices[position_of_cheapest:]
			if len(subset_of_prices) == 1:
				#we have reached the end point or the prices are exhausted
				if len(stock_prices) == 1:
					break
				stock_prices.pop(position_of_cheapest)
				continue
			largest_in_subset = max(subset_of_prices)
			temp_profit = largest_in_subset - actual_element
			if temp_profit > profit:
				profit = temp_profit
			stock_prices.pop(position_of_cheapest)
		return profit

	def stock_price_bruteFroce(self,stock_prices):
		profit = 0
		for i in range(len(stock_prices)-1):
			for j in range(i+1,len(stock_prices)):
				if stock_prices[j] - stock_prices[i] > profit:
					profit = stock_prices[j] - stock_prices[i]
		return profit

	def stock_price_constantTime(self,stock_prices):
		profit = 0
		min_price = float("inf")
		for price in stock_prices:
			min_price = min(price,min_price)
			diff = price - min_price
			profit = max(profit,diff)
		return profit



if __name__ == "__main__":
	# x = ArrayMethods()
	# arr = [310,315,275,295,260,270,290,230,255,250]
	# print(x.stock_price(arr))