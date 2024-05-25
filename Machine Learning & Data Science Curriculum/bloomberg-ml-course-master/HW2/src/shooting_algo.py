import numpy as np
import pdb


def shooting_algo(
    X, y, theta_init=None, lambda_reg=1, max_iter=1000, tol=1e-8, method="rand"
):
    """
    Implement stochastic gradient descent for the lasso objective

    This particular implementation performs coordinate descent aka
    the 'shooting algorithm'. A closed form solution exists for the
    objective over a single variable. Sequentially minimizing each of
    the variables in turn decreases the objective at each step.

    Args:
        X - the feature vector, 2D numpy array of size (num_instances, num_features)
        y - the label vector, 1D numpy array of size (num_instances)
        theta - a warm start solution
        lambda_reg - the regularization coefficient
        num_iter - number of epochs (i.e number of times) to go through the whole training set

    Returns:
        theta_hist - the history of parameter vector, 3D numpy array of size (num_iter, num_features)
        loss_hist - the history of regularized loss function vector, 2D numpy array of size (num_iter,)
    """

    n, d = X.shape
    loss_hist = np.zeros(max_iter)
    theta_hist = np.zeros((max_iter, d))

    if theta_init is None:
        A = np.vstack([X, np.sqrt(lambda_reg) * np.eye(d)])
        b = np.vstack([y[:, None], np.zeros((d, 1))])
        theta = np.linalg.lstsq(A, b, rcond=None)[0].squeeze()
    else:
        theta = theta_init

    indices = np.arange(d)
    prev_loss = compute_square_loss(X, y, theta)
    for iteration in range(max_iter):
        if method.lower() == "rand":
            np.random.shuffle(indices)
        for index, coord in enumerate(indices):
            x_col = X[:, coord]
            residual = y - X.dot(theta)
            a = 2 * np.sum(np.square(x_col))
            c = 2 * np.dot(x_col, residual) + theta[coord] * a
            if a == 0:
                theta[coord] = 0
            else:
                theta[coord] = soft_threshold(c / a, lambda_reg / a)

        squared_loss = compute_square_loss(X, y, theta)
        regularization_loss = np.linalg.norm(theta, ord=1)
        loss_hist[iteration] = squared_loss + lambda_reg * regularization_loss
        theta_hist[iteration, :] = theta

        if np.abs(loss_hist[iteration] - prev_loss) <= tol:
            break

        prev_loss = loss_hist[iteration]

    return theta_hist[: iteration + 1, :], loss_hist[: iteration + 1]


def soft_threshold(x, y):
    """Returns the subgradient of the LASSO objective function

    Args :
        x : float
        y : float

    Returns
        float
    """
    return np.sign(x) * np.maximum(np.abs(x) - y, 0)


def compute_square_loss(X, y, theta):
    """Compute the sum of squared errors"""
    return np.sum(np.square(X.dot(theta) - y))


def lasso_regularization_path(
    X_train, y_train, X_val, y_val, lambdas=None, max_iter=1000
):
    """Compute the validation loss for different values of the regularization parameter

    Args :
        X_train : ndarray
            Feature matrix of size (num_instances, num_features)
        y_train : ndarray
            Instance labels of size (num_instances,)
        X_val :
            Validation feature matrix
        y_val :
            Validation labels

    Returns :
        ndarray
    """
    if lambdas is None:
        lambda_max = 2 * np.linalg.norm(np.dot(X_train.T, y_train), ord=np.inf)
        lambdas = 10 ** np.linspace(-6, np.log10(lambda_max), 10)

    prev_theta = None
    loss_traj = []
    for index, reg_param in enumerate(lambdas):
        theta_hist, loss_hist = shooting_algo(
            X_train, y_train, theta_init=prev_theta, lambda_reg=reg_param
        )
        loss_traj.append(compute_square_loss(X_val, y_val, theta_hist[-1, :]))
        prev_theta = theta_hist[-1, :]

    return loss_traj
