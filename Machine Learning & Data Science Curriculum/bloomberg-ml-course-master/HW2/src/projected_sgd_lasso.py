import numpy as np
import pdb
from numpy import zeros, ones


def projected_batch_grad_desc_lasso(
    X, y, theta_init=None, alpha=0.1, lambda_reg=1, num_iter=1000
):
    _, num_features = X.shape

    if theta_init is None:
        theta_pos = 0.1 * np.random.randn(num_features)
        theta_neg = 0.1 * np.random.randn(num_features)
    else:
        theta_pos = theta_init.clip(min=0)
        theta_neg = (-1.0 * theta_init).clip(min=0)

    eta0 = 0.00005
    if isinstance(alpha, float):
        alpha_func = lambda x: alpha
    elif alpha == "inv":
        alpha_func = lambda x: eta0 / x
    elif alpha == "invsqrt":
        alpha_func = lambda x: eta0 / np.sqrt(x)
    else:
        raise ValueError(str)
    loss_hist = zeros(num_iter)
    theta_hist = zeros((num_iter, num_features))

    for i in range(num_iter):

        theta = theta_pos - theta_neg
        r = X.dot(theta) - y
        theta_pos_grad_step = 2 * np.dot(X.T, r) + lambda_reg * ones(num_features)
        theta_neg_grad_step = -2 * np.dot(X.T, r) + lambda_reg * ones(num_features)
        a = alpha_func(i + 1)

        # take gradient step
        theta_pos = theta_pos - a * theta_pos_grad_step
        theta_neg = theta_neg - a * theta_neg_grad_step

        # project onto nonnegative orthant
        theta_pos = np.maximum(theta_pos, np.zeros_like(theta_pos))
        theta_neg = np.maximum(theta_neg, np.zeros_like(theta_neg))

        theta_hist[i, :] = theta_pos - theta_neg
        regularization_loss = np.linalg.norm(theta_hist[i, :], ord=1)
        data_loss = compute_square_loss(X, y, theta_hist[i, :])
        loss_hist[i] = data_loss + lambda_reg * regularization_loss

    return theta_hist, loss_hist


def projected_sgd_lasso(X, y, theta_init=None, alpha=0.1, lambda_reg=1, num_iter=1000):
    """
    Implement stochastic gradient descent for the lasso objective

    This particular implementation doubles the number of variables in
    the problem by splitting theta into its positive and negative components.
    SGD proceeds normally except for an extra step that projects the parameter
    vector back onto the nonnegative orthant after each gradient step.

    Args:
        X - the feature vector, 2D numpy array of size (num_instances, num_features)
        y - the label vector, 1D numpy array of size (num_instances)
        alpha - string or float. step size in gradient descent
                NOTE: In SGD, it's not always a good idea to use a fixed step size. Usually it's set to 1/sqrt(t) or 1/t
                if alpha is a float, then the step size in every iteration is alpha.
                if alpha == "1/sqrt(t)", alpha = 1/sqrt(t)
                if alpha == "1/t", alpha = 1/t
        lambda_reg - the regularization coefficient
        num_iter - number of epochs (i.e number of times) to go through the whole training set

    Returns:
        theta_hist - the history of parameter vector, 3D numpy array of size (num_iter, num_features)
        loss_hist - the history of regularized loss function vector, 2D numpy array of size(num_iter)
    """

    num_instances, num_features = X.shape
    if theta_init is None:
        theta_pos = 0.1 * np.random.randn(num_features)
        theta_neg = 0.1 * np.random.randn(num_features)
    else:
        theta_pos = theta_init.clip(min=0)
        theta_neg = (-1.0 * theta_init).clip(min=0)

    loss_hist = zeros(num_iter)
    theta_hist = zeros((num_iter, num_features))

    indices = np.arange(num_instances)

    cnt = 1
    for i in range(num_iter):
        np.random.shuffle(indices)
        for j, index in enumerate(indices):
            x = X[index, :]
            theta = theta_pos - theta_neg
            residual = np.dot(x, theta) - y[index]
            theta_pos_sgd_step = 2 * residual * x + lambda_reg * ones(num_features)
            theta_neg_sgd_step = -2 * residual * x + lambda_reg * ones(num_features)

            # take gradient step
            theta_pos = theta_pos - alpha * theta_pos_sgd_step
            theta_neg = theta_neg - alpha * theta_neg_sgd_step

            # project onto nonnegative orthant
            theta_pos = np.maximum(theta_pos, np.zeros_like(theta_pos))
            theta_neg = np.maximum(theta_neg, np.zeros_like(theta_neg))
            cnt += 1

        theta_hist[i, :] = theta_pos - theta_neg
        regularization_loss = np.linalg.norm(theta_hist[i, :], ord=1)
        data_loss = compute_square_loss(X, y, theta_hist[i, :])
        loss_hist[i] = data_loss + lambda_reg * regularization_loss

    return theta_hist, loss_hist


def compute_square_loss(X, y, theta):
    return np.sum(np.square(X.dot(theta) - y))
