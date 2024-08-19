from bisect import bisect_left
import math


class Search:
    def __init__(self):
        pass

    def binary_search(self, target, sequence):
        start = 0
        end = len(sequence) - 1

        while start <= end:
            mid = start + (end - start) // 2

            if sequence[mid] > target:
                end = mid - 1
            elif sequence[mid] < target:
                start = mid + 1
            else:
                return mid

        return -1

    def order_agnostic_binary_search(self, target, sequence):
        start = 0
        end = len(sequence) - 1

        is_ascending = sequence[start] < sequence[end]

        while start <= end:
            mid = start + (end - start) // 2

            if target == sequence[mid]:
                return mid

            if is_ascending:
                if target < sequence[mid]:
                    end = mid - 1
                else:
                    start = mid + 1
            else:
                if target < sequence[mid]:
                    start = mid + 1
                else:
                    end = mid - 1

        return -1

    def jump_search(self, target, sequence):
        length = len(sequence)
        jump = int(math.sqrt(length))
        left, right = 0, 0
        while left < length and sequence[left] <= target:
            right = min(length - 1, left + jump)
            if sequence[left] <= target and sequence[right] >= target:
                break
            left += jump
        if left >= length or sequence[left] > target:
            return -1
        right = min(length - 1, right)
        i = left
        while i <= right and sequence[i] <= target:
            if sequence[i] == target:
                return i
            i += 1
        return -1

    def fibonacci_search(self, target, sequence):
        fibM_minus_2 = 0
        fibM_minus_1 = 1
        fibM = fibM_minus_1 + fibM_minus_2
        while fibM < len(sequence):
            fibM_minus_2 = fibM_minus_1
            fibM_minus_1 = fibM
            fibM = fibM_minus_1 + fibM_minus_2
        index = -1
        while fibM > 1:
            i = min(index + fibM_minus_2, (len(sequence) - 1))
            if sequence[i] < target:
                fibM = fibM_minus_1
                fibM_minus_1 = fibM_minus_2
                fibM_minus_2 = fibM - fibM_minus_1
                index = i
            elif sequence[i] > target:
                fibM = fibM_minus_2
                fibM_minus_1 = fibM_minus_1 - fibM_minus_2
                fibM_minus_2 = fibM - fibM_minus_1
            else:
                return i
        if (
            fibM_minus_1
            and index < (len(sequence) - 1)
            and sequence[index + 1] == target
        ):
            return index + 1
        return -1

    def interpolation_search(self, target, sequence):
        low = 0
        high = len(sequence) - 1
        while low <= high and target >= sequence[low] and target <= sequence[high]:
            index = low + int(
                (
                    (float(high - low) / (sequence[high] - sequence[low]))
                    * (target - sequence[low])
                )
            )
            if sequence[index] == target:
                return index
            if sequence[index] < target:
                low = index + 1
            else:
                high = index - 1
        return -1


class SortedCollection(Search):
    def __init__(self, iterable=(), key=None):
        self._given_key = key
        key = (lambda x: x) if key is None else key
        decorated = sorted((key(item), item) for item in iterable)
        self._keys = [k for k, item in decorated]
        self._items = [item for k, item in decorated]
        self._key = key

    def __getitem__(self, i):
        # Gets the element by index
        return self._items[i]

    def __iter__(self):
        return iter(self._items)

    def insert(self, item):
        "Insert a new item.  If equal keys are found, add to the left"
        k = self._key(item)
        i = bisect_left(self._keys, k)
        self._keys.insert(i, k)
        self._items.insert(i, item)

    def search(self, target, algorithm="binary_search"):
        methods = [x for x in dir(self) if "search" in x]
        if algorithm not in methods:
            raise Exception(
                "Not an acceptable algorithm, select one of the following: {}".format(
                    methods
                )
            )

        result = getattr(self, algorithm)(target, self._items)

        return result
