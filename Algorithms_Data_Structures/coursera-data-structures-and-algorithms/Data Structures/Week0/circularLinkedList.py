from singleyLinkedList import Node, LinkedList


class CircularLinkedList(LinkedList):
    """
    Think of a circular linked is as some sort of ring.
    An object on the ring can be thought of as the node in the list.

    """

    def __init__(self):
        super().__init__()

    def append(self, data):
        if not self.head:
            self.head = Node(data)
            self.head.next = self.head
        else:
            new_node = Node(data)
            cur = self.head
            while cur.next != self.head:
                cur = cur.next
            cur.next = new_node
            new_node.next = self.head

    def get_list(self):
        currhead = self.head
        while currhead:
            print(currhead.value)
            currhead = currhead.next
            yield currhead.value
            if currhead == self.head:
                break

    def prepend(self, element):
        curr = self.head
        new_node = Node(element)
        new_node.next = self.head
        if not self.head:  # Insert at front if this is the first element.
            new_node.next = new_node
        else:
            while curr.next != self.head:
                curr = curr.next
            curr.next = new_node
        self.head = new_node

    def remove_node(self, element):
        if self.head:
            if self.head.value == element:
                cur = self.head
                while cur.next != self.head.next:
                    cur = cur.next
                if self.head == self.head.next:  # if its the only node in the list
                    self.head = None
                else:
                    cur.next = (
                        self.head.next
                    )  # point to the node that comes after the head
                    self.head = self.head.next  # declare the head to be this new head
            else:
                curr = self.head
                prev = None
                while curr.next != self.head:
                    prev = curr
                    curr = curr.next
                    if curr.value == element:
                        prev.next = curr.next
                        curr = curr.next

    def __len__(self):
        cur = self.head
        count = 1  # start at 1 because we are stopping at last node
        while cur.next != self.head:
            count += 1
            cur = cur.next
        return count

    def split_list(self):
        size = len(self)
        if size == 0:
            return
        if size == 1:
            return self.head

        mid = size // 2
        count = 0
        prev = None
        cur = self.head

        # first half of the list
        while cur and count < mid:  # stop when you hit the midway
            count += 1
            prev = cur
            cur = cur.next
        prev.next = (
            self.head
        )  # end of the first half, assign the last node's next to be the head

        # second half of the list
        split_list = CircularLinkedList()
        while cur.next != self.head:
            split_list.append(cur.value)
            cur = cur.next
        split_list.append(cur.value)
        print([x for x in split_list.get_list()])
        return split_list

    def josephsons_problem(self, step):
        if not self.head:
            return
        if self.head.next == self.head:
            return self.head.value

        cur = self.head
        prev = None
        i = 0
        while True:
            count = step
            while count > 0:
                prev = cur
                cur = cur.next
                count -= 1
            cur = cur.next
            self.head = cur
            prev.next = cur
            if cur.next == self.head:
                break
        return cur.value

    def is_circular(self):
        if self.head:
            if self.head.next == self.head:
                return True

            cur = self.head
            while cur:
                if cur.next == self.head:
                    return True
                cur = cur.next
                if not cur.next:
                    return False


if __name__ == "__main__":
    x = CircularLinkedList()
    x.append(1)
    x.append(2)
    x.append(3)
    x.append(4)
    # x.append(10)
    # x.append(11)
    # x.append(2)
    # x.append(40)
    print(x.is_circular())
