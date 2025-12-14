import math


class BinarySearch:
    def binary_search(self, arr, value):
        mid = len(arr) // 2
        if arr[mid] == value:
            return True
        if mid == 0:
            return False
        elif arr[mid] > value:
            return self.binary_search(arr[:mid], value)
        else:
            return self.binary_search(arr[mid:], value)

    def binary_search_iterative(self, arr, value):
        """assumes arr is sorted in ascending order"""
        while True:
            mid = len(arr) // 2
            if value == arr[mid]:
                return True
            if mid == 0:
                return False
            elif value < arr[mid]:
                arr = arr[:mid]
            else:
                arr = arr[mid:]
        return False

    def linear_search(self, arr, value):
        for i in range(len(arr)):
            if arr[i] == value:
                return True
        return False

    def closestNumber(self, arr, value):
        if not arr:
            return
        if len(arr) == 1:
            return arr[0]
        for i in range(len(arr)):
            if arr[i] >= value:
                return arr[i]
        return arr[-1]

    def closest_binary_search(self, arr, value):
        diff = float("inf")
        closest = None
        while True:
            mid = len(arr) // 2
            if mid == 0:
                break
            if arr[mid] == value:
                return value
            elif arr[mid] > value:
                tempdiff = abs(arr[mid] - value)
                tempclosest = arr[mid]
                arr = arr[:mid]
            elif arr[mid] < value:
                tempdiff = abs(arr[mid] - value)
                tempclosest = arr[mid]
                arr = arr[mid:]

            if tempdiff < diff:
                diff = tempdiff
                closest = tempclosest
        return {"closest": closest, "difference": diff}

    def find_fixed_point(self, A):
        low = 0
        high = len(A) - 1

        while low <= high:
            mid = (low + high) // 2

            if A[mid] < mid:
                low = mid + 1
            elif A[mid] > mid:
                high = mid - 1
            else:
                return A[mid]
        return None

    def find_uppercase_recursive(self, input_str, idx=0):
        if input_str[idx].isupper():
            return input_str[idx]
        if idx == len(input_str) - 1:
            return "No uppercase character found"
        return find_uppercase_recursive(input_str, idx + 1)


def look_and_say(sequence):
    out = []
    end = len(sequence) - 1
    while True:
        diff = False
        i = 0
        prev = None
        temp = {}
        while True:
            if not prev:
                prev = sequence[i]
                temp[prev] = 1
            else:
                temp[prev] += 1
            if i + 1 == len(sequence):
                break
            nxt = sequence[i + 1]
            i += 1
            if prev != nxt:
                diff = True
                break
        out.append(temp)
        if i + 1 == len(sequence):
            if diff:
                temp = {}
                temp[sequence[i]] = 1
                out.append(temp)
            break
        sequence = sequence[i:]
    st = ""
    for dct in out:
        k = next(iter(dct))
        v = dct[k]
        st += str(v)
        st += str(k)
    return out, st


def spreadsheet_encode_column(col_str):
    num = 0
    count = len(col_str) - 1
    for s in col_str:
        num += 26**count * (ord(s) - ord("A") + 1)
        count -= 1
    return num


def is_palindrome(s):
    i = 0
    j = len(s) - 1

    while i < j:
        while not s[i].isalnum() and i < j:
            i += 1
        while not s[j].isalnum() and i < j:
            j -= 1

        if s[i].lower() != s[j].lower():
            return False
        i += 1
        j -= 1
    return True


def is_anagram(s1, s2):
    ht = {}

    if len(s1) != len(s2):
        return False

    for i in s1:
        if i in ht:
            ht[i] += 1
        else:
            ht[i] = 1
    for i in s2:
        if i in ht:
            ht[i] -= 1
        else:
            ht[i] = 1
    for i in ht:
        if ht[i] != 0:
            return False
    return True


if __name__ == "__main__":
    # arr = [1,2,3,10,14,15,16]
    # A1 = [1, 2, 4, 5, 6, 6, 8, 9]
    # A2 = [2, 5, 6, 7, 8, 8, 9]
    # x = BinarySearch()
    # print(x.closest_binary_search(A1,11))
    # print(x.closest_binary_search(A2,4))
    # x = "12223311"
    # print(look_and_say(x))
    print(spreadsheet_encode_column("AA"))
