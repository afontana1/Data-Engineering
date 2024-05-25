from sklearn.base import BaseEstimator, RegressorMixin
from kernel import *
import functools


def train_kernel_ridge_regression(X, y, kernel, l2reg):
    n, _ = X.shape
    K = kernel(X, X)
    alpha = np.linalg.lstsq(K + l2reg * np.eye(n), y, rcond=-1)[0]

    return Kernel_Machine(kernel, X, alpha)


class KernelRidgeRegression(BaseEstimator, RegressorMixin):
    """sklearn wrapper for our kernel ridge regression"""

    def __init__(self, kernel="RBF", sigma=1, degree=2, offset=1, l2reg=1):
        self.kernel = kernel
        self.sigma = sigma
        self.degree = degree
        self.offset = offset
        self.l2reg = l2reg

    def fit(self, X, y=None):
        """
        This should fit classifier. All the 'work' should be done here.
        """
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

        self.kernel_machine_ = train_kernel_ridge_regression(X, y, self.k, self.l2reg)

        return self

    def predict(self, X, y=None):
        try:
            getattr(self, "kernel_machine_")
        except AttributeError:
            raise RuntimeError("You must train classifer before predicting data!")

        return self.kernel_machine_.predict(X)

    def score(self, X, y=None):
        """get the average square error"""
        residual = self.predict(X) - y
        return (np.square(residual)).mean()
