# python3
# Task. In this task your goal is to implement a simple phone book manager. It should be able to process the following types of user’s queries:
# 1. add number name. It means that the user adds a person with name "name" and phone number
# "number" to the phone book. If there exists a user with such number already, then your manager
# has to overwrite the corresponding name.
# 2. del number. It means that the manager should erase a person with number "number" from the phone
# book. If there is no such person, then it should just ignore the query.
# 3∙ find number. It means that the user looks for a person with phone number "number". The manager
# should reply with the appropriate name, or with string “not found" (without quotes) if there is
# no such person in the book.
# Input Format. There is a single integer N in the first line — the number of queries. It’s followed by N
# lines, each of them contains one query in the format described above.
# Output Format. Print the result of each find query — the name corresponding to the phone number or
# “not found" (without quotes) if there is no person in the phone book with such phone number. Output
# one result per line in the same order as the find queries are given in the input.


def hash_num(number):  # Standard implementation of an integer hash function
    a, b, p, m = 34, 2, 10**8 + 19, 200000
    return ((a * number + b) % p) % m


class Query:
    def __init__(self, query):
        self.type = query[
            0
        ]  # For each query, self.type includes 3 operations: "add", "find" and "del"
        self.number = int(query[1])  # Phone number in each query
        self.hash_number = hash_num(self.number)  # Hash the phone number
        if self.type == "add":
            self.name = query[
                2
            ]  # For "add" operation, the query has 3 elements and the last element in name


def read_queries():  # Read input data
    n = int(input())
    return [Query(input().split()) for i in range(n)]


def write_responses(result):  # Write output
    print("\n".join(result))


def process_queries_fast(queries):
    result, contacts = list(), dict()
    for cur_query in queries:

        if cur_query.type == "add":  # Add a new contact to hash table
            if (
                cur_query.hash_number in contacts
            ):  # If hash number is already in the dictionary
                for contact in contacts.get(
                    cur_query.hash_number
                ):  # If query phone number appears in the list, update name and break the loop
                    if contact.number == cur_query.number:
                        contact.name = cur_query.name
                        break
                else:  # if query phone number does not appear in the list, append it
                    contacts[cur_query.hash_number].append(cur_query)
            else:  # if hash number does not appear in the dictionary, update the hash table with new hash number and append the phone number
                contacts.update({cur_query.hash_number: list()})
                contacts[cur_query.hash_number].append(cur_query)

        elif cur_query.type == "del":  # Del a contact in the dictionary
            if (
                cur_query.hash_number in contacts
            ):  # If the hash number is found in the contact
                for i in range(len(contacts.get(cur_query.hash_number))):
                    if (
                        contacts[cur_query.hash_number][i].number == cur_query.number
                    ):  # If the phone number is matched, pop it and break the loop
                        contacts[cur_query.hash_number].pop(i)
                        break

        else:  # Find a contact in the dictionary
            response = "not found"
            if (
                cur_query.hash_number in contacts
            ):  # If the hash number is found in the contact
                for contact in contacts[cur_query.hash_number]:
                    if (
                        contact.number == cur_query.number
                    ):  # If the phone number is matched, record the name and break the loop
                        response = contact.name
                        break
            result.append(response)
    return result


if __name__ == "__main__":
    write_responses(process_queries_fast(read_queries()))
