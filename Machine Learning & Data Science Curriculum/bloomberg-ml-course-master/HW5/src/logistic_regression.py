import numpy as np
from scipy.optimize import minimize
import functools


def log_loss(theta, X, y, l2_param=1):
    """
    Args:
        theta: 1D numpy array of size num_features
        X: 2D numpy array of size (num_instances, num_features)
        y: 1D numpy array of size num_instances
        l2_param: regularization parameter

    Returns:
        objective: scalar value of objective function
    """
    margin = -y * X.dot(theta)
    data_loss = np.mean(np.logaddexp(np.zeros_like(margin), margin))
    reg_loss = l2_param * np.sum(np.square(theta))

    return data_loss + reg_loss


def fit_logistic_reg(X, y, objective_function, l2_param=1, theta_init=None):
    """
    Args:
        X: 2D numpy array of size (num_instances, num_features)
        y: 1D numpy array of size num_instances
        objective_function: function returning the value of the objective
        l2_param: regularization parameter

    Returns:
        optimal_theta: 1D numpy array of size num_features
    """
    _, d = X.shape
    if theta_init is None:
        theta_init = np.zeros(d)

    result = minimize(
        functools.partial(objective_function, X=X, y=y, l2_param=l2_param), theta_init
    )

    return result.x
