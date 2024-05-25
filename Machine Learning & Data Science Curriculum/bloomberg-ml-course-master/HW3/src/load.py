import os
import numpy as np
import pickle
import random

"""
Note:  This code is just a hint for people who are not familiar with text processing in python. There is no obligation to use this code, though you may if you like. 
"""


def folder_list(path, label):
    """
    PARAMETER PATH IS THE PATH OF YOUR LOCAL FOLDER
    """
    filelist = os.listdir(path)
    review = []
    for infile in filelist:
        file = os.path.join(path, infile)
        r = read_data(file)
        r.append(label)
        review.append(r)
    return review


def read_data(file):
    """
    Read each file into a list of strings.
    Example:
    ["it's", 'a', 'curious', 'thing', "i've", 'found', 'that', 'when', 'willis', 'is', 'not', 'called', 'on',
    ...'to', 'carry', 'the', 'whole', 'movie', "he's", 'much', 'better', 'and', 'so', 'is', 'the', 'movie']
    """
    f = open(file)
    lines = f.read().split(" ")
    symbols = '${}()[].,:;+-*/&|<>=~" '
    words = map(
        lambda Element: Element.translate(str.maketrans("", "", symbols)).strip(), lines
    )
    words = filter(None, words)
    return list(words)


def shuffle_data(pos_path=None, neg_path=None):
    """
    pos_path is where you save positive review data.
    neg_path is where you save negative review data.
    """
    if pos_path is None:
        pos_path = "data/pos"
    if neg_path is None:
        neg_path = "data/neg"

    pos_review = folder_list(pos_path, 1)
    neg_review = folder_list(neg_path, -1)

    review = pos_review + neg_review
    random.shuffle(review)
    file_name = "pickle_data.pkl"
    with open(file_name, "wb") as f:
        pickle.dump(review, f)


"""
Now you have read all the files into list 'review' and it has been shuffled.
Save your shuffled result by pickle.
*Pickle is a useful module to serialize a python object structure. 
*Check it out. https://wiki.python.org/moin/UsingPickle
"""
