# python3
# Task. In this task your goal is to implement a hash table with lists chaining. You are already given the
# number of buckets m and the hash function. It is a polynomial hash function.
# Your program should support the following kinds of queries:
# 1. add string — insert string into the table. If there is already such string in the hash table, then just ignore the query.
# 2. del string — remove string from the table. If there is no such string in the hash table, then just ignore the query.
# 3. find string — output “yes" or “no" (without quotes) depending on whether the table contains string or not.
# 4. check i — output the content of the i-th list in the table. Use spaces to separate the elements of the list. If i-th list is empty, output a blank line.
# Input Format. There is a single integer m in the first line — the number of buckets you should have. The next line contains the number of queries N.
# It’s followed by N lines, each of them contains one query in the format described above.
# Output Format. Print the result of each of the find and check queries, one result per line, in the same
# order as these queries are given in the input.


class Query:  # An object Query
    def __init__(self, query):
        self.type = query[0]  # It can be "add", "del", "find", "check"
        if (
            self.type == "check"
        ):  # If it's a "check" command, the following character is a number
            self.ind = int(query[1])  # query hashes
        else:  # Otherwise, it's a string
            self.s = query[1]


class QueryProcessor:  # An object Query Processor
    _multiplier = 263
    _prime = 1000000007

    def __init__(self, bucket_count):
        self.bucket_count = bucket_count  # backet_count is the number of hash keys, used in string hashing
        self.elems = dict()  # a hash table: {hashed_string: string}

    def _hash_func(self, s):  # Standard implementation of polynomial hashing
        ans = 0
        for c in reversed(s):
            ans = (
                ans * self._multiplier + ord(c)
            ) % self._prime  # ord() maps string to integer using the Unicode
        return ans % self.bucket_count  # Number of hashes is at most "bucket_count"

    def write_search_result(self, was_found):  # Write boolean output for "find" command
        print("yes" if was_found else "no")

    def write_chain(self, chain):  # Write output string for "check" command
        print(" ".join(chain))

    def read_query(self):  # Read input queries
        return Query(input().split())

    def process_query(self, query):
        if query.type == "check":  # "check" command query
            if (
                query.ind in self.elems
            ):  # Find the chain in hash table with hash key == input number after "check" command, output the words in reversed order
                self.write_chain(reversed(self.elems[query.ind]))
            else:  # If such key does not exist, output an empty string
                self.write_chain("")
        else:
            hashed_string = self._hash_func(
                query.s
            )  # For other cases, input is a string but not a number. Hash the string first
            ind = -1
            if (
                hashed_string in self.elems
            ):  # If the string is found in the hash chain, get the index. Otherwise, index = -1 as default
                if query.s in self.elems[hashed_string]:
                    ind = self.elems[hashed_string].index(query.s)

            if query.type == "find":  # "find" command query
                self.write_search_result(
                    ind != -1
                )  # If the string is found, the index is not -1

            elif query.type == "add":  # "add" command query
                if (
                    ind == -1
                ):  # If the string is not found, check if the hash value is found. If so, append it. If not, create a new hash chain using "hashed_string" as key
                    if hashed_string in self.elems:
                        self.elems[hashed_string].append(query.s)
                    else:
                        self.elems.update({hashed_string: [query.s]})
            else:  # "del" command query
                if (
                    ind != -1
                ):  # Pop the index from hash chain, it takes at most O(m) using a list
                    self.elems[hashed_string].pop(ind)

    def process_queries(self):
        n = int(input())
        for i in range(n):
            self.process_query(self.read_query())


if __name__ == "__main__":
    bucket_count = int(input())
    proc = QueryProcessor(bucket_count)
    proc.process_queries()
