import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.exceptions import NotFittedError
from utils import zero_one, feature_map, sgd


class MulticlassSVM(BaseEstimator, ClassifierMixin):
    """Implements a Multiclass SVM estimator"""

    def __init__(
        self,
        n_out: int,
        lam: float = 1.0,
        n_classes: int = 3,
        delta=zero_one,
        psi=feature_map,
    ):
        """Creates a MulticlassSVM estimator

        :param n_out: number of class-sensitive features produced by psi
        :param lam: l2 regularization parameter
        :param num_classes: number of classes (assumed numbered 0,..,num_classes-1)
        :param delta: class-sensitive loss function taking two arguments (i.e., target margin)
        :param psi: class-sensitive feature map taking two arguments
        """
        self.n_out = n_out
        self.lam = lam
        self.n_classes = n_classes
        self.delta = delta
        self.psi = lambda X, y: psi(X, y, n_classes)
        self.is_fit = False

    def subgradient(self, x, y, w):
        """Computes the subgradient at a given data point x,y

        :param x: sample input
        :param y: sample class
        :param w: parameter vector
        :return: returns subgradient vector at given x,y,w
        """
        true_featmap = self.psi(x, y)
        feat_maps = np.zeros((self.n_classes, true_featmap.size))
        for i in np.arange(self.n_classes):
            feat_maps[i, :] = true_featmap - self.psi(x, i)
        class_scores = 1 - feat_maps.dot(w)
        pred_label = np.argmax(class_scores)
        dreg = 2 * self.lam * w
        ddata = -feat_maps[pred_label, :]

        return dreg + ddata

    def fit(self, X, y, eta=0.1, epochs=10000):
        """Fits multiclass SVM

        :param X: array-like, shape = [num_samples,num_inFeatures], input data
        :param y: array-like, shape = [num_samples,], input classes
        :param eta: learning rate for SGD
        :param T: maximum number of iterations
        :return: self
        """
        self.coef_ = sgd(X, y, self.n_out, self.subgradient, eta, epochs)
        self.is_fit = True
        return self

    def decision_function(self, X):
        """Returns the score on each input for each class. Assumes
        that fit has been called.

        :param X : array-like, shape = [n_samples, n_in]
        :return: array-like, shape = [n_samples, n_classes] giving scores for each sample,class pairing
        """
        if not self.is_fit:
            raise NotFittedError(
                f"This {self.__class__.__name__} instance is not fitted yet. "
                "Call 'fit' with appropriate arguments before using this method."
            )
        W = self.coef_.reshape((self.n_classes, -1)).T
        return X @ W

    def predict(self, X):
        """Predict the class with the highest score.

        :param X: array-like, shape = [n_samples, n_in], input data to predict
        :return array-like, shape = [n_samples,], class labels predicted for each data point
        """
        class_scores = self.decision_function(X)
        return np.argmax(class_scores, axis=1)
