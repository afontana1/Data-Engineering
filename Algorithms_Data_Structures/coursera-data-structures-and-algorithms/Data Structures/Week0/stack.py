"""
implementation of a stack and some algorithms with it
"""


class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        self.items.pop()

    def get_stack(self):
        return self.items

    def peak(self):
        top_value = None
        if self.items:
            top_value = self.items[-1]
        return top_value

    def is_empty(self):
        return True if not self.items else False


def balanced_Parenthesis(parenth):

    mapping = {"{": "}", "(": ")", "[": "]"}
    stack = Stack()
    for bracket in parenth:
        if bracket in mapping.keys():
            stack.push(bracket)
        elif bracket in mapping.values():
            peak = stack.peak()
            if not peak:
                return False
            value = mapping[peak]
            if value == bracket:
                stack.pop()
            else:
                return False

    return True if stack.is_empty() else False


def is_match(p1, p2):
    if p1 == "(" and p2 == ")":
        return True
    elif p1 == "{" and p2 == "}":
        return True
    elif p1 == "[" and p2 == "]":
        return True
    else:
        return False


def is_paren_balanced(paren_string):
    s = Stack()
    is_balanced = True
    index = 0

    while index < len(paren_string) and is_balanced:
        paren = paren_string[index]
        if paren in "([{":
            s.push(paren)
        else:
            if s.is_empty():
                is_balanced = False
            else:
                top = s.pop()
                if not is_match(top, paren):
                    is_balanced = False
        index += 1

    if s.is_empty() and is_balanced:
        return True
    else:
        return False


def reverse_string(string):
    s = Stack()
    rev_string = ""
    for st in string:
        s.push(st)

    while not s.is_empty():
        rev_string += s.peak()
        s.pop()
    return rev_string


input_str = "muM rU"


def integer_to_binary(integer):
    quotient = integer
    binary = ""
    s = Stack()
    while quotient != 0:
        remainder = quotient % 2
        quotient = quotient // 2
        s.push(remainder)

    while not s.is_empty():
        binary += str(s.peak())
        s.pop()

    return binary


if __name__ == "__main__":
    print("String : (((({})))) Balanced or not?")
    print(balanced_Parenthesis("(((({}))))"))

    print("String : [][]]] Balanced or not?")
    print(balanced_Parenthesis("[][]]]"))

    print("String : [][] Balanced or not?")
    print(balanced_Parenthesis("[][]"))

    print(reverse_string(input_str))
    print(integer_to_binary(242))
