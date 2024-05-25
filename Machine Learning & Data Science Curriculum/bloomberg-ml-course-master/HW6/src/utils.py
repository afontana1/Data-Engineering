from collections import Counter
import numpy as np


def compute_entropy(label_array):
    """Calulate the entropy of given label list

    :param label_array: a numpy array of labels shape = (n,)
    :return: entropy value
    """
    n_elems = label_array.size
    if n_elems == 0:
        return 0.0
    _, elem_counts = np.unique(label_array, return_counts=True)
    probs = elem_counts / n_elems

    return -np.sum(probs * np.log2(probs + 1e-7))


def compute_gini(label_array):
    """Calulate the gini index of label list

    :param label_array: a numpy array of labels shape = (n,)
    :return: gini index value
    """
    n_elems = label_array.size
    if n_elems == 0:
        return 0.0
    _, elem_counts = np.unique(label_array, return_counts=True)
    probs = elem_counts / n_elems

    return 1 - np.sum(np.square(probs))


def most_common_label(y):
    """Find most common label

    :param y: numpy array of labels shape=(n,)
    :return: most frequent label
    """
    label_cnt = Counter(y)
    most_common_label, _ = label_cnt.most_common(1)[0]

    return most_common_label


def mean_absolute_deviation_around_median(y):
    """Calulate the mean absolute deviation around the median of a given target list

    :param y: a numpy array of targets shape = (n, 1)
    :return: mean absolute deviation from the median
    """
    m = np.median(y)
    y_centered = y - m
    mae = np.mean(np.abs(y_centered))

    return mae


def pseudo_residual_L2(train_target, train_predict):
    """Compute the pseudo-residual for half the L2 norm based on
    current predicted value

    :param train_target:
    :param train_predict:
    :return: pseudo-residual of the l2 norm
    """
    return train_target - train_predict


def sigmoid(x):
    """Numerically-stable sigmoid function.

    https://stackoverflow.com/questions/3985619/how-to-calculate-a-logistic-sigmoid-function-in-python
    :param x:
    """
    z = np.exp(-x)
    return 1 / (1 + z)


def pseudo_residual_logistic(train_target, train_predict):
    """Compute the pseudo-residual for half the L2 norm based on
    current predicted value

    :param train_target:
    :param train_predict:
    :return: pseudo-residual of the l2 norm
    """
    return train_target * sigmoid(-train_target * train_predict)


def zero_one(y: np.ndarray, a: np.ndarray):
    """Computes the zero-one loss

    :param y: output class
    :param a: predicted class
    :return: 1 if different, 0 if same
    """
    return int(y != a)


def feature_map(X, y, n_classes: int):
    """Computes the class-sensitive features

    :param X: array-like, shape = [n_samples, n_in] or [n_in,], input features for input data
    :param y: a target class (in range 0,..,n_classes - 1)
    :param n_classes: number of target classes
    :return: array-like, shape = [n_samples, n_out], the class sensitive features for class y
    """
    n_samples, n_in = (1, X.size) if X.ndim == 1 else X.shape
    n_out = n_classes * n_in
    psi = np.zeros((n_samples, n_out))

    if n_samples == 1:
        start_index = y * n_in
        end_index = start_index + n_in
        psi[0, start_index:end_index] = X
    else:
        for i in range(n_samples):
            start_index = y[i] * n_in
            end_index = start_index + n_in
            psi[i, start_index:end_index] = X[i, :]
    return psi


def sgd(X, y, n_out: int, subgd, eta: float = 0.1, epochs: int = 1000):
    """Runs subgradient descent, and outputs resulting parameter vector

    :param X: array-like, shape = [n_samples, n_features], input training data
    :param y: array-like, shape = [n_samples,], class labels
    :param n_out: number of class-sensitive features
    :param subgd: function taking x,y and giving subgradient of objective
    :param eta: learning rate for SGD
    :param T: maximum number of iterations
    :return: vector of weights
    """
    n_samples, _ = X.shape
    weights = np.zeros(n_out)

    indices = np.arange(n_samples)
    for i in range(epochs):
        np.random.shuffle(indices)
        for j in indices:
            weights -= eta * subgd(X[j, :], y[j], weights)
    return weights
