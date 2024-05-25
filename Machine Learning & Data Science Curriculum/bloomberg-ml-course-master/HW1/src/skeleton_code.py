import os
import sys
import pdb
import pandas as pd
import logging
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cross_validation import train_test_split
from numpy import zeros, ones

### Assignment Owner: Tian Wang

#######################################
#### Normalization


def feature_normalization(train, test):
    """Rescale the data so that each feature in the training set is in
    the interval [0,1], and apply the same transformations to the test
    set, using the statistics computed on the training set.

    Args:
        train - training set, a 2D numpy array of size (num_instances, num_features)
        test  - test set, a 2D numpy array of size (num_instances, num_features)
    Returns:
        train_normalized - training set after normalization
        test_normalized  - test set after normalization

    """
    feat_max = np.amax(train, axis=0, keepdims=True)
    feat_min = np.amin(test, axis=0, keepdims=True)

    constant_features = (feat_max == feat_min).squeeze()
    feat_max_drop_const = feat_max[:, ~constant_features]
    feat_min_drop_const = feat_min[:, ~constant_features]
    train_drop_const = train[:, ~constant_features]
    test_drop_const = test[:, ~constant_features]

    normalizer = feat_max_drop_const - feat_min_drop_const
    train_normalized = (train_drop_const - feat_min_drop_const) / normalizer
    test_normalized = (test_drop_const - feat_min_drop_const) / normalizer

    return train_normalized, test_normalized


########################################
#### The square loss function


def compute_square_loss(X, y, theta):
    """
    Given a set of X, y, theta, compute the square loss for predicting y with X*theta

    Args:
        X - the feature vector, 2D numpy array of size (num_instances, num_features)
        y - the label vector, 1D numpy array of size (num_instances)
        theta - the parameter vector, 1D array of size (num_features)

    Returns:
        loss - the square loss, scalar
    """
    predict = X.dot(theta[:, None])
    squared_error = np.square(y[:, None] - predict)
    loss = np.mean(squared_error)

    return loss


########################################
### compute the gradient of square loss function
def compute_square_loss_gradient(X, y, theta):
    """
    Compute gradient of the square loss (as defined in compute_square_loss), at the point theta.

    Args:
        X - the feature vector, 2D numpy array of size (num_instances, num_features)
        y - the label vector, 1D numpy array of size (num_instances)
        theta - the parameter vector, 1D numpy array of size (num_features)

    Returns:
        grad - gradient vector, 1D numpy array of size (num_features)
    """
    m = X.shape[0]
    r = X.dot(theta[:, None]) - y[:, None]
    grad = 2.0 / m * np.dot(X.T, r)  # 2/m X^T * (X * theta - y)

    return grad.squeeze()


###########################################
### Gradient Checker
# Getting the gradient calculation correct is often the trickiest part
# of any gradient-based optimization algorithm.  Fortunately, it's very
# easy to check that the gradient calculation is correct using the
# definition of gradient.
# See http://ufldl.stanford.edu/wiki/index.php/Gradient_checking_and_advanced_optimization
def grad_checker(X, y, theta, epsilon=0.01, tolerance=1e-4):
    """Implement Gradient Checker
    Check that the function compute_square_loss_gradient returns the
    correct gradient for the given X, y, and theta.

    Let d be the number of features. Here we numerically estimate the
    gradient by approximating the directional derivative in each of
    the d coordinate directions:
    (e_1 = (1,0,0,...,0), e_2 = (0,1,0,...,0), ..., e_d = (0,...,0,1)

    The approximation for the directional derivative of J at the point
    theta in the direction e_i is given by:
    ( J(theta + epsilon * e_i) - J(theta - epsilon * e_i) ) / (2*epsilon).

    We then look at the Euclidean distance between the gradient
    computed using this approximation and the gradient computed by
    compute_square_loss_gradient(X, y, theta).  If the Euclidean
    distance exceeds tolerance, we say the gradient is incorrect.

    Args:
        X - the feature vector, 2D numpy array of size (num_instances, num_features)
        y - the label vector, 1D numpy array of size (num_instances)
        theta - the parameter vector, 1D numpy array of size (num_features)
        epsilon - the epsilon used in approximation
        tolerance - the tolerance error

    Return:
        A boolean value indicate whether the gradient is correct or not

    """

    true_gradient = compute_square_loss_gradient(X, y, theta)  # the true gradient
    num_features = theta.shape[0]
    approx_gradient = np.zeros(num_features)  # Initialize the gradient we approximate
    identity = np.eye(num_features)

    for i in range(num_features):
        v = identity[i, :]
        forward = compute_square_loss_gradient(X, y, theta + epsilon * v)
        backward = compute_square_loss_gradient(X, y, theta - epsilon * v)
        approx_gradient[i] = (forward - backward) / (2 * epsilon)

    return np.linalg.norm(true_gradient - approx_gradient) <= tolerance


#################################################
### Generic Gradient Checker
def generic_gradient_checker(
    X, y, theta, objective_func, gradient_func, epsilon=0.01, tolerance=1e-4
):
    """
    The functions takes objective_func and gradient_func as parameters. And check whether gradient_func(X, y, theta) returned
    the true gradient for objective_func(X, y, theta).
    Eg: In LSR, the objective_func = compute_square_loss, and gradient_func = compute_square_loss_gradient
    """
    true_gradient = gradient_func(X, y, theta)
    num_features = theta.shape[0]
    approx_gradient = np.zeros(num_features)
    identity = np.eye(num_features)

    for i in range(num_features):
        v = identity[i, :]
        forward = objective_func(X, y, theta + epsilon * v)
        backward = objective_func(X, y, theta - epsilon * v)
        approx_gradient[i] = (forward - backward) / (2 * epsilon)

    return np.linalg.norm(true_gradient - approx_gradient) <= tolerance


####################################
#### Batch Gradient Descent
def batch_grad_descent(
    X, y, alpha=0.1, backtracking=False, num_iter=1000, check_gradient=False
):
    """
    In this question you will implement batch gradient descent to
    minimize the square loss objective

    Args:
        X - the feature vector, 2D numpy array of size (num_instances, num_features)
        y - the label vector, 1D numpy array of size (num_instances)
        alpha - step size in gradient descent
        num_iter - number of iterations to run
        check_gradient - a boolean value indicating whether checking the gradient when updating

    Returns:
        theta_hist - store the the history of parameter vector in iteration, 2D numpy array of size (num_iter+1, num_features)
                    for instance, theta in iteration 0 should be theta_hist[0], theta in ieration (num_iter) is theta_hist[-1]
        loss_hist - the history of objective function vector, 1D numpy array of size (num_iter+1)
    """
    num_instances, num_features = X.shape
    theta_hist = np.zeros((num_iter + 1, num_features))  # initialize theta_hist
    loss_hist = np.zeros(num_iter + 1)  # initialize loss_hist
    stepsize_hist = np.zeros(num_iter)

    theta_hist[0, :] = np.random.randn(num_features)
    loss_hist[0] = compute_square_loss(X, y, theta_hist[0, :])
    if backtracking:
        a, b = 0.4, 0.5

        for i in range(num_iter):
            t = 1
            theta0 = theta_hist[i, :]
            f0 = compute_square_loss(X, y, theta0)
            desc_direction = -compute_square_loss_gradient(X, y, theta0)
            gradient = -desc_direction
            slope = np.dot(gradient, desc_direction)

            while True:
                fnext = compute_square_loss(X, y, theta0 + t * desc_direction)
                if fnext <= (f0 + t * a * slope):
                    theta_hist[i + 1, :] = theta0 + t * desc_direction
                    loss_hist[i + 1] = compute_square_loss(X, y, theta_hist[i + 1, :])
                    stepsize_hist[i] = t
                    break
                else:
                    t *= b
    else:
        stepsize_hist = alpha * ones(num_iter)
        for i in range(0, num_iter):
            curr_theta = theta_hist[i, :]
            dtheta = compute_square_loss_gradient(X, y, curr_theta)
            theta_hist[i + 1, :] = curr_theta - alpha * dtheta
            loss_hist[i + 1] = compute_square_loss(X, y, theta_hist[i + 1, :])

    return theta_hist, loss_hist, stepsize_hist


####################################
###Q2.4b: Implement backtracking line search in batch_gradient_descent
###Check http://en.wikipedia.org/wiki/Backtracking_line_search for details
# TODO


###################################################
### Compute the gradient of Regularized Batch Gradient Descent
def compute_regularized_square_loss_gradient(X, y, theta, lambda_reg):
    """
    Compute the gradient of L2-regularized square loss function given X, y and theta

    Args:
        X - the feature vector, 2D numpy array of size (num_instances, num_features)
        y - the label vector, 1D numpy array of size (num_instances)
        theta - the parameter vector, 1D numpy array of size (num_features)
        lambda_reg - the regularization coefficient

    Returns:
        grad - gradient vector, 1D numpy array of size (num_features)
    """
    return compute_square_loss_gradient(X, y, theta) + 2 * lambda_reg * theta


###################################################
### Batch Gradient Descent with regularization term
def regularized_grad_descent(
    X, y, alpha=0.1, lambda_reg=1, backtracking=False, num_iter=1000
):
    """
    Args:
        X - the feature vector, 2D numpy array of size (num_instances, num_features)
        y - the label vector, 1D numpy array of size (num_instances)
        alpha - step size in gradient descent
        lambda_reg - the regularization coefficient
        numIter - number of iterations to run

    Returns:
        theta_hist - the history of parameter vector, 2D numpy array of size (num_iter+1, num_features)
        loss_hist - the history of loss function without the regularization term, 1D numpy array.
    """
    (num_instances, num_features) = X.shape
    theta_hist = zeros((num_iter + 1, num_features))  # initialize theta_hist
    loss_hist = zeros(num_iter + 1)  # initialize loss_hist
    stepsize_hist = zeros(num_iter + 1)

    theta_hist[0, :] = zeros(num_features)
    data_loss = compute_square_loss(X, y, theta_hist[0, :])
    reg_loss = np.sum(np.square(theta_hist[0, :]))
    loss_hist[0] = data_loss + lambda_reg * reg_loss

    if backtracking:
        a, b = 0.4, 0.5

        for i in range(num_iter):
            t = 1
            theta0 = theta_hist[i, :]
            f0 = compute_square_loss(X, y, theta0)
            desc_direction = -compute_regularized_square_loss_gradient(
                X, y, theta0, lambda_reg
            )
            gradient = -desc_direction
            slope = np.dot(gradient, desc_direction)

            while True:
                fnext = compute_square_loss(X, y, theta0 + t * desc_direction)
                if fnext <= (f0 + t * a * slope):
                    theta_hist[i + 1, :] = theta0 + t * desc_direction
                    loss_hist[i + 1] = compute_square_loss(X, y, theta_hist[i + 1, :])
                    stepsize_hist[i] = t
                    break
                else:
                    t *= b
    else:
        for i in range(0, num_iter):
            curr_theta = theta_hist[i, :]
            dtheta = compute_regularized_square_loss_gradient(
                X, y, curr_theta, lambda_reg
            )
            theta_hist[i + 1, :] = curr_theta - alpha * dtheta
            loss_hist[i + 1] = compute_square_loss(X, y, theta_hist[i + 1, :])

    return theta_hist, loss_hist, stepsize_hist


#############################################
## Visualization of Regularized Batch Gradient Descent
##X-axis: log(lambda_reg)
##Y-axis: square_loss

#############################################
### Stochastic Gradient Descent
def stochastic_grad_descent(X, y, alpha=0.1, lambda_reg=1, num_iter=1000):
    """
    In this question you will implement stochastic gradient descent with a regularization term

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
        theta_hist - the history of parameter vector, 3D numpy array of size (num_iter, num_instances, num_features)
        loss hist - the history of regularized loss function vector, 2D numpy array of size(num_iter, num_instances)
    """
    num_instances, num_features = X.shape
    theta = ones(num_features)  # Initialize theta

    theta_hist = zeros((num_iter, num_instances, num_features))  # Initialize theta_hist
    loss_hist = zeros((num_iter, num_instances))  # Initialize loss_hist
    indices = np.arange(num_instances)

    eta0 = 0.05
    if isinstance(alpha, float):
        alpha_func = lambda x: alpha
    elif alpha == "inv":
        alpha_func = lambda x: eta0 / x
    elif alpha == "invsqrt":
        alpha_func = lambda x: eta0 / np.sqrt(x)
    elif alpha == "rational":
        alpha_func = lambda x: eta0 * 0.05 / (1 + eta0 * 0.05 * lambda_reg * x)
    else:
        raise ValueError(str)

    cnt = 1
    for i in range(num_iter):
        np.random.shuffle(indices)
        for j, index in enumerate(indices):
            a = alpha_func(cnt)
            ypred = np.dot(theta, X[index, :])
            r = ypred - y[index]
            sgd_step = 2 * a * (r * X[index, :] + lambda_reg * theta)

            theta -= sgd_step
            theta_hist[i, j, :] = theta
            data_loss = compute_square_loss(X, y, theta)
            reg_loss = np.sum(np.square(theta))
            loss_hist[i, j] = data_loss + lambda_reg * reg_loss
            cnt += 1

    return theta_hist, loss_hist


################################################
### Visualization that compares the convergence speed of batch
###and stochastic gradient descent for various approaches to step_size
##X-axis: Step number (for gradient descent) or Epoch (for SGD)
##Y-axis: log(objective_function_value) and/or objective_function_value


def main():
    # Loading the dataset
    print("loading the dataset")

    curr_path = os.path.dirname(os.path.realpath(__file__))
    data_file = os.path.join(curr_path, "..", "data", "data.csv")
    df = pd.read_csv(data_file, delimiter=",")
    X = df.values[:, :-1]
    y = df.values[:, -1]

    print("Split into Train and Test")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=100, random_state=10
    )

    print("Scaling all to [0, 1]")
    X_train, X_test = feature_normalization(X_train, X_test)
    X_train = np.hstack((X_train, np.ones((X_train.shape[0], 1))))  # Add bias term
    X_test = np.hstack((X_test, np.ones((X_test.shape[0], 1))))  # Add bias term

    iters = 1000
    plt.figure(figsize=(10, 10))
    for a in [0.05, 0.01, 0.005, 0.001]:
        theta_hist, loss_hist, _ = batch_grad_descent(
            X_train, y_train, alpha=a, num_iter=iters
        )
        plt.plot(np.arange(iters + 1), loss_hist, label=r"$\alpha$={}".format(a))

    plt.title("Batch Gradient Descent Training loss")
    plt.grid(True, which="major")
    plt.grid(True, which="minor")
    plt.legend()

    plt.xlabel("Iteration")
    plt.ylabel(r"$||X\theta - y||^2$")
    plt.savefig(os.path.join("..", "imgs", "training_loss.png"))
    plt.close()


if __name__ == "__main__":
    main()
