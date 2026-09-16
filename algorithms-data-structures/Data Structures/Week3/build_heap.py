# python3
# Input Format. The first line of the input contains single integer n. The next line contains n space-separated
# integers a[i].
# Output Format. The first line of the output should contain single integer m — the total number of swaps.
# m must satisfy conditions 0 <= m <= 4*n. The next m lines should contain the swap operations used
# to convert the array a into a heap. Each swap is described by a pair of integers i, j — the 0-based
# indices of the elements to be swapped. After applying all the swaps in the specified order the array
# must become a heap, that is, for each i where 0 <= i <= n − 1 the following conditions must be true:
# 1. If 2*i + 1 <= n − 1, then a[i] < a[2*i + 1].
# 2. If 2*i + 2 <= n − 1, then a[i] < a[2*i + 2].
# Note that all the elements of the input array are distinct. Note that any sequence of swaps that has
# length at most 4*n and after which your initial array becomes a correct heap will be graded as correct.


class Heap:  # A binary min-heap
    def __init__(self, arr):
        self.arr = arr  # Input array
        self.swap = []  # Store swap operations

    def LeftChild(i):  # return the index of left child
        return 2 * i + 1

    def RightChild(i):  # return the index of right child
        return 2 * i + 2

    def SiftDown(self, i):
        minIndex = i
        l = Heap.LeftChild(
            i
        )  # Compare if left child has a key less than that of input node.
        if l < len(self.arr):
            if self.arr[l] < self.arr[minIndex]:
                minIndex = l
        r = Heap.RightChild(i)
        if r < len(self.arr):
            if (
                self.arr[r] < self.arr[minIndex]
            ):  # Compare if left child has a key less than that of input node or left child.
                minIndex = r
        if i != minIndex:
            self.swap.append((i, minIndex))  # Record swapping operation
            self.arr[i], self.arr[minIndex] = (
                self.arr[minIndex],
                self.arr[i],
            )  # Swap input node with the children with the minimal key
            Heap.SiftDown(
                self, minIndex
            )  # Do it recursively until no more swapping can be done


def BuildHeap(arr):
    size = len(arr)
    heap = Heap(arr)
    for i in reversed(
        range(0, size // 2)
    ):  # The last n / 2 are leaves. We start at the second last level and push the minimum key up for each subtree
        heap.SiftDown(i)
    return heap.swap


def main():
    n = int(input())
    data = list(map(int, input().split()))
    assert len(data) == n

    swap = BuildHeap(data)
    print(len(swap))
    if len(swap) > 0:
        for i, j in swap:
            print(i, j)


if __name__ == "__main__":
    main()
