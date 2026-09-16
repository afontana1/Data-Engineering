class Chain:
    """Method chaining"""

    def __init__(self, number):
        self.number = number

    def add(self, number):
        self.number += number
        return self

    def subtract_one(self):
        self.number -= 1
        return self

    def multiply(self, number):
        self.number *= number
        return self


x = Chain(number=10)
x.add(number=5).subtract_one()


class Reverse:
    """Iterator for looping over a sequence backwards."""

    def __init__(self, seq):
        self.data = seq
        self.index = len(seq)

    def __iter__(self):
        return self

    def __next__(self):
        if self.index == 0:
            raise StopIteration
        self.index = self.index - 1
        return self.data[self.index]


# Custom context managers


class Example(object):
    def __init__(self, attribute):
        print("__init__ called")
        self.attribute = attribute

    def __enter__(self):
        print("__enter__ called")
        self.other_attribute = self.attribute.upper()
        return self.other_attribute

    def __exit__(self, exc_type, exc_value, traceback):
        print("__exit__ called")
        print(self.other_attribute.lower())

    def __iter__(self):
        yield from self.attribute


class AnotherExample:
    def __init__(self, content):
        self.content = content
        self._index = 0

    def __enter__(self):
        return self.content

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < len(self.content):
            thing = self.addresses[self._index]
            self._index += 1
            return thing
        else:
            raise StopIteration


with Example(attribute="Some thing ") as an_example:
    print(an_example)
    for thing in an_example:
        print(thing)

with AnotherExample(content="Some thing ") as an_example:
    print(an_example)
    for thing in an_example:
        print(thing)


import uuid

# list is iterable
names = ["Elon", "Guido", "Bjern"]
for name in names:
    print(name)
    # Elon
    # Guido
    # Bjern


class UUIDIterator:
    """
    Iterator for generating UUID.
    """

    def __init__(self, limit):
        self._limit = limit
        self._index = 0

    def __next__(self):
        if self._index < self._limit:
            self._index += 1
            return uuid.uuid1()
        raise StopIteration


class UUIDRange:
    """
    Iterable object that uses Iterator.
    """

    def __init__(self, count=1):
        self.count = count

    def __iter__(self):
        """
        Return iterator object.
        :return: iterator-object (UUIDIterator)
        """
        return UUIDIterator(self.count)


for uuid_ in UUIDRange(3):
    print(uuid_)
    # 67e56182-d3fb-11e9-bca0-701ce791b04a
    # 67e56402-d3fb-11e9-bca0-701ce791b04a
    # 67e564e8-d3fb-11e9-bca0-701ce791b04a
