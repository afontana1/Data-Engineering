"""
With all of the linear structures, the differences
occur basically when and where you can append or
pop objects from the ADT
"""


class Stack:
    """
	Implements stack ADT
	Stacks adhere to the LIFO principle of ordering
	"""

    def __init__(self):
        self.base = []

    def add(self, elements):
        """
		adds an element to the end of the array
		"""
        self.base.append(elements)

    def empty(self):
        """
		checks if the stack is empty
		"""
        return True if not self.base else False

    def remove(self):
        """
		removes the last element added to the stack
		throws error if empty 
		"""
        if self.empty():
            raise ValueError("empty stack, cant remove anything")
        else:
            self.base.pop(len(self.base) - 1)

    def peak(self):
        if self.empty():
            raise ValueError("no elements in stack, so no peak")
        else:
            return self.base[-1]


class reverseStack:
    """
	implements reversed stack
	"""

    def __init__(self):
        self.base = []

    def add(self, item):
        self.base.insert(0, item)

    def empty(self):
        return True if not self.base else False

    def remove(self):
        if self.empty():
            raise ValueError("the stack is empty")
        else:
            self.base.pop(0)

    def peak(self):
        if self.empty():
            raise ValueError("the stack is empty")
        else:
            return self.base[0]


def test_stack(x):
    """
	test some of the functionality of the stack
	"""
    for i in range(0, 100):
        x.add(i)

    while not x.empty():
        x.remove()

    assert len(x.base) == 0


x = Stack()
print(test_stack(x))


class Queue:
    """
	Implements queue ADT, following FIFO principle
	"""

    def __init__(self):
        self.base = []

    def empty(self):
        return True if not self.base else False

    def add(self, element):
        self.base.insert(0, element)

    def remove(self):
        if not self.empty():
            self.base.pop(len(self.base) - 1)
        else:
            raise ValueError("empty")

    def length(self):
        return len(self.base)


x = Queue()
x.add(2)
x.add(3)
print(x.base)
x.remove()
print(x.base)


class Dequeue:
    """
	Similar to Queue, except you can insert into beginning or end
	and can remove from beginning or end
	"""

    def __init__(self):
        self.base = []

    def empty(self):
        return self.base == []

    def add_beginning(self, element):
        self.base.insert(0, element)

    def add_end(self, element):
        self.base.append(element)

    def remove_beginning(self):
        if not self.empty():
            self.base.pop(0)
        else:
            raise ValueError("empty")

    def remove_End(self):
        if not self.empty():
            self.base.pop(len(self.base) - 1)
        else:
            raise ValueError("empty")


x = Dequeue()
x.add_beginning(3)
print(x.empty())



#Linked List

class Node():
    def __init__(self,initdata):
        self.data = initdata
        self.next = None

    def getData(self):
        return self.data

    def getNext(self):
        return self.next

    def setData(self,newdata):
        self.data = newdata

    def setNext(self,newnext):
        self.next = newnext


class LinkedList:
    '''
    Built from a collection of nodes
    Each node will hold reference to the next 
    node in the list
    '''

    def __init__(self):
        """initialize the starting point"""
        self.head = None

    def empty(self):
        return self.head == None

    def add(self,item):
        temp = Node(item)
        temp.setNext(self.head)
        self.head = temp

     def size(self):
        current = self.head
        count = 0
        while current != None:
            count = count + 1
            current = current.getNext()

        return count

    def search(self,item):
        current = self.head
        found = False
        while current != None and not found:
            if current.getData() == item:
                found = True
            else:
                current = current.getNext()

        return found

    def remove(self,item):
        current = self.head
        previous = None
        found = False
        while not found:
            if current.getData() == item:
                found = True
            else:
                previous = current
                current = current.getNext()

        if previous == None:
            self.head = current.getNext()
        else:
            previous.setNext(current.getNext())