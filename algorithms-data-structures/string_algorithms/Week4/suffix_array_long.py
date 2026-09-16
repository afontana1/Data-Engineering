# python3
import sys


def sort_characters(S):
    dict_help = {"$": 0, "A": 1, "C": 2, "G": 3, "T": 4}
    size_alphabet = 5
    order = [0] * len(S)
    count = [0] * size_alphabet
    for i in range(len(S)):
        count[dict_help[S[i]]] += 1
    for i in range(1, size_alphabet):
        count[i] += count[i - 1]
    for i in reversed(range(len(S))):
        c = dict_help[S[i]]
        count[c] -= 1
        order[count[c]] = i
    return order


def compute_char_classes(S, order):
    class_ = [0] * len(S)
    class_[order[0]] = 0
    for i in range(1, len(S)):
        if S[order[i]] != S[order[i - 1]]:
            class_[order[i]] = class_[order[i - 1]] + 1
        else:
            class_[order[i]] = class_[order[i - 1]]
    return class_


def sort_doubled(S, L, order, class_):
    count = [0] * len(S)
    newOrder = [0] * len(S)
    for i in range(len(S)):
        count[class_[i]] += 1
    for i in range(1, len(S)):
        count[i] += count[i - 1]
    for i in reversed(range(len(S))):
        start = (order[i] - L + len(S)) % len(S)
        cl = class_[start]
        count[cl] -= 1
        newOrder[count[cl]] = start
    return newOrder


def update_classes(newOrder, class_, L):
    n = len(newOrder)
    newClass = [0] * n
    newClass[newOrder[0]] = 0
    for i in range(1, n):
        cur = newOrder[i]
        prev = newOrder[i - 1]
        mid = (cur + L) % n
        midPrev = (prev + L) % n
        if (class_[cur] != class_[prev]) or (class_[mid] != class_[midPrev]):
            newClass[cur] = newClass[prev] + 1
        else:
            newClass[cur] = newClass[prev]
    return newClass


def build_suffix_array(text):
    """
    Build suffix array of the string text and
    return a list result of the same length as the text
    such that the value result[i] is the index (0-based)
    in text where the i-th lexicographically smallest
    suffix of text starts.
    """
    order = sort_characters(text)
    class_ = compute_char_classes(text, order)
    L = 1
    while L < len(text):
        order = sort_doubled(text, L, order, class_)
        class_ = update_classes(order, class_, L)
        L *= 2
    # Implement this function yourself
    return order


if __name__ == "__main__":
    text = sys.stdin.readline().strip()
    #    text = 'AACGATAGCGGTAGA$'
    print(" ".join(map(str, build_suffix_array(text))))
