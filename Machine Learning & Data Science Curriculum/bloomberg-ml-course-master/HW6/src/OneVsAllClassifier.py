import numpy as np
from sklearn.exceptions import NotFittedError
from sklearn.base import BaseEstimator, ClassifierMixin, clone


class OneVsAllClassifier(BaseEstimator, ClassifierMixin):
    """
    One-vs-all classifier
    We assume that the classes will be the integers 0,..,(n_classes-1).
    We assume that the estimator provided to the class, after fitting, has a "decision_function" that
    returns the score for the positive class.
    """

    def __init__(self, estimator, n_classes):
        """Constructed with the number of classes and an estimator (e.g. an
        SVM estimator from sklearn)

        :param estimator: binary base classifier used
        :param n_classes: number of classes
        """
        self.n_classes = n_classes
        self.estimators = [clone(estimator) for _ in range(n_classes)]
        self.is_fit = False

    def fit(self, X, y=None):
        """This should fit one classifier for each class.

        self.estimators[i] should be fit on class i vs rest
        :param X: array-like, shape = [n_samples,n_features], input data
        :param y: array-like, shape = [n_samples,] class labels
        :return: returns self
        """
        for i, estimator in enumerate(self.estimators):
            z = 2.0 * (y == i) - 1.0
            estimator.fit(X, z)
        self.is_fit = True
        return self

    def decision_function(self, X):
        """Returns the score of each input for each class

        Assumes that the given estimator also implements the decision_function method (which sklearn SVMs do),
        and that fit has been called.

        :param X: array-like, shape = [n_samples, n_features] input data
        :return: array-like, shape = [n_samples, n_classes]
        """
        if not self.is_fit:
            raise NotFittedError(
                f"This {self.__class__.__name__} instance is not fitted yet. "
                "Call 'fit' with appropriate arguments before using this method."
            )
        if not hasattr(self.estimators[0], "decision_function"):
            raise AttributeError(
                "Base estimator doesn't have a decision_function attribute."
            )

        class_scores = np.zeros((X.shape[0], self.n_classes))
        for i, estimator in enumerate(self.estimators):
            class_scores[:, i] = estimator.decision_function(X)

        return class_scores

    def predict(self, X):
        """Predict the class with the highest score

        :param X: array-like, shape = [n_samples,n_features] input data
        :return: array-like, shape = [n_samples,] the predicted classes for each input
        """
        class_scores = self.decision_function(X)
        return np.argmax(class_scores, axis=1)
