'''
Runtime Complexity
Best Case: 
𝑂(𝑛)
This occurs when the input list is already sorted. 
The inner while loop is never entered, so the algorithm runs in linear time.
Average Case: 
𝑂(𝑛2)
On average, each insertion requires shifting about half of the sorted portion of the list, 
resulting in quadratic time complexity.
Worst Case: 
𝑂(𝑛2)
This occurs when the input list is sorted in reverse order. 
The inner while loop runs i times for each element, resulting in quadratic time complexity.

Correctness
The algorithm maintains the following invariants:

At the start of each iteration of the outer loop, the subarray arr[0..i-1] is sorted.
Each element in the subarray arr[0..i-1] is less than or equal to arr[i].
By the end of the last iteration, the entire array is sorted. 
The correctness of the insertion sort algorithm can be proven using induction:

Base Case: For i = 1, the subarray arr[0] is trivially sorted.
Inductive Step: Assume the subarray arr[0..i-1] is sorted before iteration i. 
During iteration i, arr[i] is inserted into the correct position in the sorted subarray, 
resulting in the subarray arr[0..i] being sorted.
'''
def insertion_sort(arr):
    # Traverse from 1 to len(arr)
    for i in range(1, len(arr)):
        key = arr[i]  # The current element to be inserted into the sorted portion
        j = i - 1  # The last index of the sorted portion of the array

        # Move elements of arr[0..i-1], that are greater than key,
        # to one position ahead of their current position
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        
        # Insert the key at the correct position
        arr[j + 1] = key

    return arr

if __name__ == "__main__":
    arr = [12, 11, 13, 5, 6]
    sorted_arr = insertion_sort(arr)
    print("Sorted array:", sorted_arr)