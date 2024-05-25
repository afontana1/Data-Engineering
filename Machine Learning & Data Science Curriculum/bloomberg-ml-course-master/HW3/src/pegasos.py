import os
import numpy as np
import logging
from collections import Counter

from util import *


class Pegasos(object):
    def __init__(self, lambda_reg=1):
        self._lambda_reg = lambda_reg

    def fit(self, X_train, y_train, num_epochs=5, train_type="default"):
        self._w = {}
        self._train_features = X_train
        self._train_labels = y_train
        self._train_loss = [svm_loss(X_train, y_train, self._w, self._lambda_reg)]
        N = len(X_train)

        indices = np.arange(N)
        if train_type == "default":
            t = 1
            for _ in range(num_epochs):
                np.random.shuffle(indices)
                for j in indices:
                    t += 1
                    eta = 1 / (self._lambda_reg * t)
                    x = X_train[j]
                    y = y_train[j]

                    if y * dot_product(self._w, x) < 1:
                        linear_combination(1 - 1 / t, self._w, eta * y, x)
                    else:
                        scalar_multiply(1 - 1 / t, self._w)
                curr_loss = svm_loss(X_train, y_train, self._w, self._lambda_reg)
                self._train_loss.append(curr_loss)

        elif train_type == "optimized":
            t = 1
            s = 1
            W = {}
            for _ in range(num_epochs):
                np.random.shuffle(indices)
                for j in indices:
                    t += 1
                    x = X_train[j]
                    y = y_train[j]
                    margin = y * s * dot_product(W, x)
                    s *= 1 - 1 / t
                    eta = 1 / (self._lambda_reg * t)

                    if margin < 1:
                        increment(W, 1 / s * eta * y, x)

                self._w = dict((k, s * v) for k, v in W.items())
                self._train_loss.append(
                    svm_loss(X_train, y_train, self._w, self._lambda_reg)
                )
        else:
            raise ValueError

    def score(self, X_test):
        return [dot_product(self._w, x) for x in X_test]

    def predict(self, X_test):
        scores = self.score(X_test)
        predictions = []
        for s in scores:
            if s > 0:
                predictions.append(1)
            elif s < 0:
                predictions.append(-1)
            else:
                if np.random.rand() < 0.5:
                    predictions.append(-1)
                else:
                    predictions.append(1)

        return predictions
