# Taken from http://web.stanford.edu/class/cs221/ Assignment #2 Support Code
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer


def dot_product(d1, d2):
    """
    @param dict d1: a feature vector represented by a mapping from a feature (string) to a weight (float).
    @param dict d2: same as d1
    @return float: the dot product between d1 and d2
    """
    if len(d1) < len(d2):
        return dot_product(d2, d1)
    else:
        return sum(d1.get(f, 0) * v for f, v in d2.items())


def scalar_multiply(scale, d):
    """
    @param float scale: value to multiply each elemnt of the vector
    @param dict d: sparse feature vector represented by a mapping from a feature (string) to a weight (float).
    """
    for f, v in d.items():
        d[f] = scale * v


def increment(d1, scale, d2):
    """
    Implements d1 += scale * d2 for sparse vectors.
    @param dict d1: the feature vector which is mutated.
    @param float scale
    @param dict d2: a feature vector.

    NOTE: This function does not return anything, but rather
    increments d1 in place. We do this because it is much faster to
    change elements of d1 in place than to build a new dictionary and
    return it.
    """
    for f, v in d2.items():
        d1[f] = d1.get(f, 0) + v * scale


def linear_combination(scale1, d1, scale2, d2):
    """
    Sets d1 = scale1 * d1 + scale2 * d2
    @param float scale1
    @param dict d1: a feature vector represented by a mapping from a feature (string) to a weight (float).
    @param float scale2
    @param dict d2: a feature vector represented by a mapping from a feature (string) to a weight (float).
    """
    scalar_multiply(scale1, d1)
    increment(d1, scale2, d2)


def bag_of_words(word_list):
    """
    Converts an example (e.g. a list of words) into a sparse
    bag-of-words representation.

    @param list word_list: words (with multiplicity) that appear in
    the document
    """
    return Counter(word_list)


def svm_loss(X, y, w, lambda_reg):
    """
    Compute the regularized SVM loss for the given weights and regularization param

    @param list X: feature vectors
    @param list y: corresponding ground truth labels
    @param dict w: sparse representaiton of parameter vector
    @param float lambda_reg: regularization strength. Larger means more regularization
    @return float
    """
    reg_loss = sum(v**2 for _, v in w.items())
    data_loss = 1 / len(X) * sum(hinge_loss(x, label, w) for x, label in zip(X, y))

    return data_loss + lambda_reg / 2 * reg_loss


def hinge_loss(x, y, w):
    """
    Compute max(0, 1- y w^Tx)

    @param list x: feature vector
    @param list y: corresponding ground truth label
    @param dict w: sparse representaiton of parameter vector
    @return float
    """

    return max([0, 1 - y * dot_product(w, x)])
