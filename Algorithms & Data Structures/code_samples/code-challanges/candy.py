import os
from collections import Counter
from typing import (
    List,
    Counter,
    Optional,
    Any,
    Mapping,
    Generator,
)

LENGTH = 4
example : str = "baaaabbcaaaaacccc"
example : str = "abcdefg"

def identify(sequence:str, start: int) -> Any:
    """Identify sequences with subsequence greater than N."""
    count, index = 1, 0
    initialization: str = sequence[start:]
    while index<=(len(initialization)-2):
        if (initialization[index] != initialization[index+1]):
            break
        count+=1
        index+=1
    return count

def find_subsequence(sequence:str,subsequence_length:int = LENGTH):
    start = 0
    while start <= len(sequence):
        count = identify(sequence=sequence, start = start)
        if count >= subsequence_length:
            return True, sequence[:start] + sequence[start+count:]
        start+=count
    return False, sequence

def collapse(sequence:str) -> str:
    while True:
        boolean, new_sequence = find_subsequence(sequence=sequence)
        if not boolean:
            break
        sequence = new_sequence
        print(sequence)
    return sequence


if __name__ == "__main__":
    print(collapse(sequence = example))