import matplotlib.pyplot as plt
from itertools import product
import numpy as np
from collections import Counter
from sklearn.base import BaseEstimator
from utils import (
    compute_entropy,
    compute_gini,
    most_common_label,
    mean_absolute_deviation_around_median,
)
from sklearn.exceptions import NotFittedError


class DecisionTree(BaseEstimator):
    def __init__(
        self,
        split_loss_function,
        leaf_value_estimator,
        depth: int = 0,
        min_sample: int = 5,
        max_depth: int = 10,
    ):
        """Initialize the decision tree classifier

        :param split_loss_function: method for splitting node
        :param leaf_value_estimator: method for estimating leaf value
        :param depth: depth indicator, default value is 0, representing root node
        :param min_sample: an internal node can be split only if it contains points more than min_smaple
        :param max_depth: restriction of tree depth
        """
        self.split_loss_function = split_loss_function
        self.leaf_value_estimator = leaf_value_estimator
        self.depth = depth
        self.min_sample = min_sample
        self.max_depth = max_depth
        self.is_fit = False

    def fit(self, X, y):
        """Fit the decision tree in place

        This should fit the tree classifier by setting the values:
        self.is_leaf
        self.split_id (the index of the feature we want to split on, if we're splitting)
        self.split_value (the corresponding value of that feature where the split is)
        self.value (the prediction value if the tree is a leaf node).

        If we are splitting the node, we should also init self.left and self.right to
        be DecisionTree objects corresponding to the left and right subtrees. These
        subtrees should be fit on the data that fall to the left and right, respectively,
        of self.split_value. This is a recursive tree building procedure.

        :param X: a numpy array of training data, shape = (n, m)
        :param y: a numpy array of labels, shape = (n,)
        :return: self
        """
        n_data, n_features = X.shape
        self.is_fit = True
        if self.depth == self.max_depth or n_data <= self.min_sample:
            self.is_leaf = True
            self.value = self.leaf_value_estimator(y)
            return self

        best_split_feature, best_split_score = 0, np.inf
        for feature in range(n_features):
            values = X[:, feature]
            sort_indices = np.argsort(values)
            sorted_values = values[sort_indices]
            sorted_labels = y[sort_indices]
            _, unique_indexes = np.unique(sorted_values, return_index=True)
            for i in unique_indexes:
                y_l, y_r = sorted_labels[:i], sorted_labels[i:]
                l_split_val = self.split_loss_function(y_l)
                r_split_val = self.split_loss_function(y_r)
                node_split_score = (
                    i / n_data * l_split_val + (1 - i / n_data) * r_split_val
                )

                if node_split_score < best_split_score:
                    best_split_score = node_split_score
                    best_split_feature = feature
                    best_split_value = sorted_values[i]

        mask = X[:, best_split_feature] < best_split_value
        n_l = np.sum(mask)
        n_r = n_data - n_l
        if n_l < self.min_sample or n_r < self.min_sample:
            self.is_leaf = True
            self.value = self.leaf_value_estimator(y)
            return self

        self.is_leaf = False
        self.split_id = best_split_feature
        self.split_value = best_split_value

        X_l, y_l = X[mask, :], y[mask]
        X_r, y_r = X[~mask, :], y[~mask]

        self.left = DecisionTree(
            self.split_loss_function,
            self.leaf_value_estimator,
            depth=self.depth + 1,
            min_sample=self.min_sample,
            max_depth=self.max_depth,
        )
        self.right = DecisionTree(
            self.split_loss_function,
            self.leaf_value_estimator,
            depth=self.depth + 1,
            min_sample=self.min_sample,
            max_depth=self.max_depth,
        )
        self.left.fit(X_l, y_l)
        self.right.fit(X_r, y_r)

        return self

    def predict_instance(self, instance):
        """Predict label by decision tree

        :param instance: numpy array with new data, shape (1, m)
        :return: whatever is returned by leaf_value_estimator for leaf containing instance
        """
        if not self.is_fit:
            raise NotFittedError(
                f"This {self.__class__.__name__} instance is not fitted yet. "
                "Call 'fit' with appropriate arguments before using this method."
            )
        elif self.is_leaf:
            return self.value
        elif instance[self.split_id] <= self.split_value:
            return self.left.predict_instance(instance)
        else:
            return self.right.predict_instance(instance)


class ClassificationTree(BaseEstimator):

    loss_function_dict = {"entropy": compute_entropy, "gini": compute_gini}

    def __init__(
        self, loss_function: str = "entropy", min_sample: int = 5, max_depth: int = 10
    ):
        """
        :param loss_function(str): loss function for splitting internal node
        :param min_sample: minimum number of data points in a leaf
        :param max_depth: maximum depth the tree can grow
        """

        self.tree = DecisionTree(
            self.loss_function_dict[loss_function],
            most_common_label,
            0,
            min_sample,
            max_depth,
        )

    def fit(self, X, y):
        self.tree.fit(X, y)
        return self

    def predict_instance(self, instance):
        return self.tree.predict_instance(instance)


class RegressionTree(BaseEstimator):
    """
    :attribute loss_function_dict: dictionary containing the loss functions used for splitting
    :attribute estimator_dict: dictionary containing the estimation functions used in leaf nodes
    """

    loss_function_dict = {"mse": np.var, "mae": mean_absolute_deviation_around_median}

    estimator_dict = {"mean": np.mean, "median": np.median}

    def __init__(
        self, loss_function="mse", estimator="mean", min_sample=5, max_depth=10
    ):
        """Initialize RegressionTree

        :param loss_function(str): loss function used for splitting internal nodes
        :param estimator(str): value estimator of internal node
        """

        self.tree = DecisionTree(
            self.loss_function_dict[loss_function],
            self.estimator_dict[estimator],
            0,
            min_sample,
            max_depth,
        )

    def fit(self, X, y):
        self.tree.fit(X, y)
        return self

    def predict_instance(self, instance):
        return self.tree.predict_instance(instance)
