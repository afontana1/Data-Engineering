from stack import Stack


class Node:
    def __init__(self, data):
        self.value = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def insert(self, element):
        new_element = Node(element)
        if not self.head:
            self.head = new_element
            return

        most_recent = self.head
        while most_recent.next:
            most_recent = most_recent.next

        most_recent.next = new_element

    def insert_after(self, element, previous_node):
        if not previous_node:
            return
        new = Node(element)
        new.next = previous_node.next
        previous_node.next = new

    def peak_last(self):
        if not self.head:
            return
        last = self.head
        while last.next:
            last = last.next
        return last.value

    def peak_next(self, element):
        return element.next.value

    def get_values(self):
        if not self.head:
            return
        cur_node = self.head
        while cur_node:
            yield cur_node.value
            cur_node = cur_node.next

    def prepend(self, element):
        new = Node(element)
        new.next = self.head
        self.head = new

    def print_list(self):
        cur_node = self.head
        while cur_node:
            print(cur_node.value)
            cur_node = cur_node.next

    def delete_by_value(self, value):
        if not self.head:
            return
        element = self.head
        if element.value == value:
            self.head = element.next
            element = None
            return

        prior = None
        while element.next:
            prior = element
            element = element.next
            if element.value == value:
                prior.next = element.next
                break

        if element is None:
            return

    def length(self):
        if not self.head:
            return None
        count = 0
        element = self.head
        while element:
            element = element.next
            count += 1
        return count

    def swap_nodes(self, key_1, key_2):
        if key_1 == key_2:
            return

        prev_1 = None
        curr_1 = self.head
        while curr_1 and curr_1.data != key_1:
            prev_1 = curr_1
            curr_1 = curr_1.next
        prev_2 = None
        curr_2 = self.head
        while curr_2 and curr_2.data != key_2:
            prev_2 = curr_2
            curr_2 = curr_2.next
        if not curr_1 or not curr_2:
            return

        if prev_1:
            prev_1.next = curr_2
        else:
            self.head = curr_2

        if prev_2:
            prev_2.next = curr_1
        else:
            self.head = curr_1
        curr_1.next, curr_2.next = curr_2.next, curr_1.next

    def reverse_list(self):
        curr_node = self.head
        previous = None
        while curr_node:
            next_node = curr_node.next
            curr_node.next = previous
            previous = curr_node
            curr_node = next_node
        self.head = previous
        return

    def merge_sorted_lists(self, llist):
        l1 = self.head
        l2 = llist.head
        s = None
        if not l1 or not l2:
            return

        if l1 and l2:
            if l1.value <= l2.value:
                s = l1
                l1 = s.next
            else:
                s = l2
                l2 = s.next
            new_head = s
        while l1 and l2:
            if l1.value <= l2.data:
                s.next = l1
                s = l1
                l2 = s.next
            else:
                s.next = l2
                s = l2
                l2 = s.next
        if not l1:
            s.next = l2
        if not l2:
            s.next = l1
        return new_head

    def delete_duplicates(self):
        if not self.head:
            return
        curr_node = self.head
        cache = []
        prev = None
        while curr_node.next:
            val = curr_node.value
            if val in cache:
                prev.next = curr_node.next
            else:
                cache.append(val)
                prev = curr_node
            curr_node = prev.next

    def nth_to_last(self, nth):
        length = self.length()
        if length:
            value = length - nth
        else:
            return
        count = 0
        target = None
        curr_node = self.head
        while curr_node:
            if count == value:
                target = curr_node
                break
            count += 1
            curr_node = curr_node.next
            if count == length:
                break
        return target.value if target else target

    def count_occurences(self, element):
        if not self.head:
            return

        count = 0
        curr_node = self.head
        while curr_node:
            if curr_node.value == element:
                count += 1
            curr_node = curr_node.next
        return count

    def count_recursive(self, element, node):
        if not node:
            return 0
        if node.value == element:
            return 1 + self.count_recursive(element, node.next)
        else:
            return self.count_recursive(element, node.next)

    def rotate(self, element):
        """rotate around the nth element"""
        if not self.head:
            return
        p, q = None, None
        i = 0
        curr_node = self.head
        while curr_node.next:
            if i == element:
                p = curr_node
            curr_node = curr_node.next
            i += 1
            if not curr_node.next:
                q = curr_node
        if not p:
            return
        q.next = self.head
        self.head = p.next
        p.next = None

    def is_palindrome(self) -> bool:
        """using stack, string, and pointers"""
        if not self.head:
            return
        is_pal = True
        s = Stack()
        curr_node = self.head
        while curr_node:
            s.push(curr_node.value)
            curr_node = curr_node.next

        curr_node = self.head
        while curr_node:
            val = s.peak()
            if curr_node.value != val:
                is_pal = False
                break
            s.pop()
            curr_node = curr_node.next

        forward = "".join(self.get_values())
        self.reverse_list()
        backward = "".join(self.get_values())
        return (forward == backward) and is_pal


def tail_to_head(ll):
    if not ll.head:
        return
    prevnode = None
    curr_node = ll.head
    while curr_node.next:
        prevnode = curr_node
        curr_node = curr_node.next

    curr_node.next = ll.head
    prevnode.next = None
    ll.head = curr_node
    ll.print_list()


def sum_two_lists(ll1, ll2):
    """sum two lists"""
    ll1.reverse_list()
    ll2.reverse_list()

    curr1, curr2 = ll1.head, ll2.head
    number1, number2 = "", ""
    while curr1:
        number1 += str(curr1.value)
        curr1 = curr1.next
    while curr2:
        number2 += str(curr2.value)
        curr2 = curr2.next
    return int(number1) + int(number2)


if __name__ == "__main__":
    llist = LinkedList()
    llist.insert("A")
    llist.insert("B")
    llist.insert("C")
    llist.insert("D")
    llist.insert("C")
    llist.insert("B")
    llist.insert("A")
    tail_to_head(llist)

    llist1 = LinkedList()
    llist2 = LinkedList()
    llist1.insert(2)
    llist1.insert(3)
    llist1.insert(4)
    llist2.insert(4)
    llist2.insert(4)
    llist2.insert(2)
    print(sum_two_lists(llist1, llist2))
