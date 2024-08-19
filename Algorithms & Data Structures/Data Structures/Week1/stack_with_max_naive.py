# python3
import sys

# Task. Implement a stack supporting the operations Push(), Pop(), and Max().
# Input Format. The first line of the input contains the number q of queries. Each of the following q lines
# specifies a query of one of the following formats: push v, pop, or max.
# Constraints. 1 <= q <= 400 000, 0 <= v <= 105.
# Output Format. For each max query, output (on a separate line) the maximum value of the stack.


class StackWithMax:
    def __init__(self):
        self.__stack = []  # An empty list to store q in the stack
        self.__max = (
            []
        )  # An empty list to keep track of the max value in the stack. The cost is double memeory requirement.

    def Push(self, a):  # Push: An element is added to the stack
        # A greedy algorithm to take maximum value from queries. Push() has O(1) operations
        self.__stack.append(a)
        if (
            self.__max == []
        ):  # If there are no record of maximum value, it is then the maximum
            self.__max.append(a)
        elif (
            a > self.__max[-1]
        ):  # If it is greater than the previous maximum value, let it be the maximum
            self.__max.append(a)
        else:  # If not, the maximum value is still the previous one
            self.__max.append(self.__max[-1])

    def Pop(self):  # Pop() also has O(1) operations
        assert len(self.__stack)
        self.__stack.pop()  # If we remove a value, then we also remove the associated maximum values
        self.__max.pop()  # If the removed value it the maximum, the maximum value will also be removed. Otherwise, it does not hurt the optimality

    def Max(self):  # It also has O(1) operations
        assert len(self.__stack)
        return self.__max[
            -1
        ]  # Greedy strategy: Always return the last element. It is a safe move because the last element is always greater than or equal to previous elements


if __name__ == "__main__":
    stack = StackWithMax()
    num_queries = int(sys.stdin.readline())

    for _ in range(num_queries):
        query = sys.stdin.readline().split()
        if query[0] == "push":
            stack.Push(int(query[1]))
        elif query[0] == "pop":
            stack.Pop()
        elif query[0] == "max":
            print(stack.Max())
        else:
            assert 0
