from typing import List


class Node:
    def __init__(self, value):
        self.prev = None
        self.value = value
        self.next = None


class doublyLinkedList:
    def __init__(self):
        self.head = None

    def append(self, value):
        """append to end of list"""
        if not self.head:
            new = Node(value)
            self.head = new
            return
        new = Node(value)
        curr = self.head
        while curr.next:
            curr = curr.next
        curr.next = new
        new.prev = curr
        new.next = None
        return

    def prepend(self, value):
        if not self.head:
            new = Node(value)
            self.head = new
            return
        new = Node(value)
        curr = self.head
        curr.prev = new
        new.next = curr
        self.head = new

    def print_list(self):
        curr = self.head
        while curr:
            print(curr.value)
            curr = curr.next

    def add_after(self, value, location):
        if not self.head:
            self.head = Node(value)
        new = Node(value)
        curr = self.head
        while curr:  # identify the node
            if curr.value == location and not curr.next:  # end of the list
                self.append(value)
                return
            elif curr.value == location:
                nxt = curr.next
                curr.next = new
                new.next = nxt
                new.prev = curr
                nxt.prev = new
                return
            curr = curr.next
        return

    def add_before(self, value, location):
        if not self.head:
            self.head = Node(value)
        new = Node(value)
        curr = self.head
        while curr:  # identify the node
            if curr.value == location and not curr.prev:  # front of the list
                self.prepend(value)
                return
            elif curr.value == location:
                prev = curr.prev
                prev.next = new
                curr.prev = new
                new.next = curr
                new.prev = prev
                return
            curr = curr.next
        return

    def delete(self, key):
        cur = self.head
        while cur:
            if cur.value == key and cur == self.head:
                # Case 1: Only node present
                if not cur.next:
                    cur = None
                    self.head = None
                    return

                # Case 2: The head of the list
                else:
                    nxt = cur.next
                    cur.next = None
                    nxt.prev = None
                    cur = None
                    self.head = nxt
                    return

            elif cur.value == key:
                # Case 3: any node in between
                if cur.next:
                    nxt = cur.next
                    prev = cur.prev
                    prev.next = nxt
                    nxt.prev = prev
                    cur.next = None
                    cur.prev = None
                    cur = None
                    return

                # Case 4: the end of the node
                else:
                    prev = cur.prev
                    prev.next = None
                    cur.prev = None
                    cur = None
                    return
            cur = cur.next

    def reverse(self):

        if not self.head:
            return
        curr = self.head
        tmp = None
        while curr:
            tmp = curr.prev
            curr.prev = curr.next
            curr.next = tmp
            curr = curr.prev
            if tmp:
                self.head = tmp.prev

    def count(self):
        if self.head:
            curr = self.head
            count = 0
            while curr:
                count += 1
                curr = curr.next
            return count
        return None

    def remove_duplicates(self):
        if self.head:
            curr = self.head
            cache = []
            while curr:
                if curr.value in cache:
                    self.delete(curr.value)
                cache.append(curr.value)
                curr = curr.next

    def sum_pairs(self, target):
        count = self.count()
        if count:
            if count < 3:
                first, second = self.head.value, self.head.next.value
                tot = first + second
                if tot == target:
                    return [(first, second)]
            sums = []
            curr = self.head
            while curr:
                val1 = curr.value
                nxt = curr.next
                while nxt:
                    val2 = nxt.value
                    if (val1 + val2) == target:
                        pair = (val1, val2)
                        if pair not in sums:
                            sums.append(pair)
                    nxt = nxt.next
                curr = curr.next
            return sums

    def print_reversed(self):
        curr = self.head
        while curr.next:
            curr = curr.next

        while curr:
            print(curr.value)
            curr = curr.prev


def maxArea(self, height: List[int]) -> int:
    water = 0
    head = 0
    tail = len(height) - 1

    for cnt in range(len(height)):

        width = abs(head - tail)

        if height[head] < height[tail]:
            res = width * height[head]
            head += 1
        else:
            res = width * height[tail]
            tail -= 1

        if res > water:
            water = res

    return water


if __name__ == "__main__":

    ll = doublyLinkedList()
    ll.prepend(2)
    ll.append(2)
    ll.append(3)
    ll.append(6)
    ll.append(1)
    ll.append(8)
    ll.append(6)
    # ll.add_after("C","B")
    # ll.print_list()
    # ll.print_list()
    # ll.print_list()
    # ll.reverse()
    # print(ll.sum_pairs(9))
    ll.print_reversed()
