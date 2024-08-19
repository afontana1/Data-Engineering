from collections import Counter


def distribute(items, num_containers, hash_function=hash):
    return Counter([hash_function(item) % num_containers for item in items])


def plot(histogram):
    for key in sorted(histogram):
        count = histogram[key]
        padding = (max(histogram.values()) - count) * " "
        print(f"{key:3} {'■' * count}{padding} ({count})")


class HashNode:
    def __init__(self, key, value):
        self.next = None
        self.key = key
        self.value = value


class HashTable:
    def __init__(self):
        self.table = [None] * 101

    def hash(self, key):
        # Generate hash from key.
        # Time O(N), Space O(1), where N is the length of key.
        hashed = 0
        for i in range(len(key)):
            hashed = (256 * hashed + ord(key[i])) % 101
        return hashed

    def add(self, key, value):
        # Add key, value.
        # Time O(1), Space O(1), where N is the num of elements in hashtable.
        bucket = self.hash(key)
        if not self.table[bucket]:
            self.table[bucket] = HashNode(key, value)
        else:
            temp = self.table[bucket]
            while temp.next:
                temp = temp.next
            temp.next = HashNode(key, value)

    def find(self, key):
        # Find value from key.
        # Time O(1), Space O(1), where N is the num of elements in hashtable.
        bucket = self.hash(key)
        if not self.table[bucket]:
            return False
        else:
            temp = self.table[bucket]
            while temp:
                if temp.key == key:
                    return temp.value
                temp = temp.next
            return False

    def delete(self, key):
        # Delete key, value.
        # Time O(1), Space O(1), where N is the num of elements in hashtable.
        bucket = self.hash(key)
        if not self.table[bucket]:
            return False
        else:
            if self.table[bucket].key == key:
                self.table[bucket] = None
            else:
                temp = self.table[bucket]
                while temp:
                    if temp.next.key == key:
                        temp.next = temp.next.next
                        return
                    temp = temp.next
                return False


class Hash_Table:
    def __init__(self):
        self.size = 11
        self.positions = [None] * self.size
        self.values = [None] * self.size

    def put(self, key, value):
        hashvalue = self.hashfn(key, len(self.positions))

        if self.positions[hashvalue] == None:
            self.positions[hashvalue] = key
            self.values[hashvalue] = value
        else:
            if self.positions[hashvalue] == key:
                self.values[hashvalue] = value  # replace
            else:
                nextposition = self.rehash(hashvalue, len(self.positions))
                while (
                    self.positions[nextposition] != None
                    and self.positions[nextposition] != key
                ):
                    nextposition = self.rehash(nextposition, len(self.positions))

            if self.positions[nextposition] == None:
                self.positions[nextposition] = key
                self.values[nextposition] = value
            else:
                self.values[nextposition] = value  # replace

    def hashfn(self, key, size):
        return key % size

    def rehash(self, oldhash, size):
        return (oldhash + 1) % size

    def get(self, key):
        startposition = self.hashfn(key, len(self.positions))

        value = None
        stop = False
        found = False
        position = startposition
        while self.positions[position] != None and not found and not stop:
            if self.positions[position] == key:
                found = True
                value = self.values[position]
            else:
                position = self.rehash(position, len(self.positions))
            if position == startposition:
                stop = True
        return value

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        self.put(key, value)


if __name__ == "__main__":
    H = Hash_Table()
    H[31] = "cow"
    H[44] = "goat"
    H[54] = "cat"
    H[17] = "tiger"
    H[77] = "bird"
    H[55] = "pig"
    H[20] = "chicken"
    H[26] = "dog"
    H[93] = "lion"

    print(H.positions)
    print(H.values)

    print(H[20])

    print(H[17])
    H[20] = "duck"
    print(H[20])
    print(H[99])
