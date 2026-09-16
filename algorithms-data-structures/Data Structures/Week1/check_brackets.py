# python3
from collections import namedtuple

Bracket = namedtuple("Bracket", ["char", "position"])
# Input Format. Input contains one string S which consists of big and small latin letters, digits, punctuation
# marks and brackets from the set []{}().
# Output Format. If the code in S uses brackets correctly, output “Success" (without the quotes). Otherwise,
# output the 1-based index of the first unmatched closing bracket, and if there are no unmatched closing
# brackets, output the 1-based index of the first unmatched opening bracket.


def are_matching(left, right):
    return (left + right) in ["()", "[]", "{}"]


def find_mismatch(text):
    opening_brackets_stack = []  # A stack implmented using list
    if (
        len(text) == 1
    ):  # If the text only contains a character, the mismatch position must be at 1
        # Improvement: Check if text[0] in '([{' or ')]}' when text may not include brackets
        return 1

    for i, char in enumerate(text):  # A loop of each character in the given text
        if char in "([{":  # If char is opening bracket, enqueue it
            opening_brackets_stack.append([char, i])
        if char in ")]}":  # Otherwise, if char is closing bracket, do the following:
            if (
                len(opening_brackets_stack) == 0
            ):  # If the queue is empty, it means that opening brackets are missing in the queue. So, return the current index as mismatch position
                return i + 1  # add one because 1-based index mentioned in the question
            else:  # Otherwise, there are something in the queue, pop it in a LIFO manner
                top = opening_brackets_stack.pop()
                if (
                    (top[0] == "[" and char != "]")
                    or (top[0] == "(" and char != ")")
                    or (top[0] == "{" and char != "}")
                ):  # Check if the opening bracket match the closing bracket. If not, return the current position
                    return i + 1
        # Ignore the cases that char is neither opening nor closing brackets
    if (
        len(opening_brackets_stack) == 0
    ):  # If all opening brackets are popped out, all brackets are matched
        return "Success"
    else:  # Otherwise, there are some opening brackets in the queue without the corresponding closing brackets, return the position indicating mismatch
        return opening_brackets_stack[0][1] + 1


def main():
    text = input()
    mismatch = find_mismatch(text)
    print(mismatch)


if __name__ == "__main__":
    main()
