import os
import numpy as np
import functools
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.metrics import accuracy_score
from kernel import *

import logging

from kernel import Kernel_Machine


class KernelPegasos(BaseEstimator, ClassifierMixin):
    def __init__(self, kernel="RBF", sigma=1, degree=2, offset=1, l2reg=1):
        self.kernel = kernel
        self.sigma = sigma
        self.degree = degree
        self.offset = offset
        self.l2reg = l2reg

    def _hinge_loss(self, k, y, alpha):
        return np.maximum(0, 1 - y * np.dot(k, alpha))

    def _svm_loss(self, K, alpha, y):
        reg_loss = self.l2reg / 2 * np.dot(alpha.T, K.dot(alpha))
        data_loss = np.mean(np.maximum(0, 1 - y * K.dot(alpha)))

        return data_loss + reg_loss

    def fit(self, X_train, y_train, num_epochs=100):
        if self.kernel == "linear":
            self.k = linear_kernel
        elif self.kernel == "RBF":
            self.k = functools.partial(RBF_kernel, sigma=self.sigma)
        elif self.kernel == "polynomial":
            self.k = functools.partial(
                polynomial_kernel, offset=self.offset, degree=self.degree
            )
        else:
            raise ValueError("Unrecognized kernel type requested.")

        self._alpha = np.random.rand(X_train.shape[0])
        self._train_data = X_train
        self._K = self.k(X_train, X_train)
        self._train_loss = [self._svm_loss(self._K, self._alpha, y_train)]
        N = X_train.shape[0]

        indices = np.arange(N)
        t = 1
        for _ in range(num_epochs):
            np.random.shuffle(indices)
            for j in indices:
                t += 1
                eta = 1 / (self.l2reg * t)
                k = self._K[j, :]
                y = y_train[j]

                self._alpha *= 1 - eta * self.l2reg
                if y * np.dot(k, self._alpha) < 1:
                    self._alpha[j] += y * eta
            curr_loss = self._svm_loss(self._K, self._alpha, y_train)
            self._train_loss.append(curr_loss)
        self._kernel_machine = Kernel_Machine(self.k, X_train, self._alpha)

        return self

    def score(self, X_test, y_test):
        return accuracy_score(y_test, self.predict(X_test))

    def predict(self, X_test):
        scores = self._kernel_machine.predict(X_test)
        predictions = np.zeros(X_test.shape[0])
        for i, s in enumerate(scores):
            if s > 0:
                predictions[i] = 1
            elif s < 0:
                predictions[i] = -1
                # predictions[i] = 0
            else:
                if np.random.rand() < 0.5:
                    predictions[i] = -1
                    # predictions[i] = 0
                else:
                    predictions[i] = 1

        return predictions
