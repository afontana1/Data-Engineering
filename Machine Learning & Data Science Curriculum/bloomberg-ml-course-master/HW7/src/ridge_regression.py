import os
import matplotlib.pyplot as plt
from sklearn.base import BaseEstimator, RegressorMixin
from sklearn.exceptions import NotFittedError
import numpy as np
import setup_problem, nodes, graph, plot_utils


class RidgeRegression(BaseEstimator, RegressorMixin):
    """Ridge regression with computation graph"""

    def __init__(self, l2_reg=1, step_size=0.005, max_num_epochs=5000):
        self.l2_reg = l2_reg
        self.max_num_epochs = max_num_epochs
        self.step_size = step_size

        # Build computation graph
        self.x = nodes.ValueNode(node_name="x")  # to hold a vector input
        self.y = nodes.ValueNode(node_name="y")  # to hold a scalar response
        self.w = nodes.ValueNode(node_name="w")  # to hold the parameter vector
        self.b = nodes.ValueNode(node_name="b")  # to hold the bias parameter (scalar)
        self.prediction = nodes.VectorScalarAffineNode(
            x=self.x, w=self.w, b=self.b, node_name="prediction"
        )

        data_loss = nodes.SquaredL2DistanceNode(
            a=self.prediction, b=self.y, node_name="square loss"
        )

        reg_loss = nodes.L2NormPenaltyNode(
            l2_reg=self.l2_reg, w=self.w, node_name="l2_penalty"
        )
        self.objective = nodes.SumNode(
            a=data_loss, b=reg_loss, node_name="ridge_objective"
        )

        # Group nodes into types to construct computation graph function
        self.inputs = [self.x]
        self.outcomes = [self.y]
        self.parameters = [self.w, self.b]

        self.graph = graph.ComputationGraphFunction(
            self.inputs, self.outcomes, self.parameters, self.prediction, self.objective
        )

    def fit(self, X, y, print_every=5):
        n_instances, n_ftrs = X.shape
        y = y.reshape(-1)

        init_parameter_values = {"w": np.zeros(n_ftrs), "b": np.array(0.0)}
        self.graph.set_parameters(init_parameter_values)

        for epoch in range(self.max_num_epochs):
            shuffle = np.random.permutation(n_instances)
            epoch_obj_tot = 0.0
            for j in shuffle:
                obj, grads = self.graph.get_gradients(
                    input_values={"x": X[j]}, outcome_values={"y": y[j]}
                )
                epoch_obj_tot += obj
                # Take step in negative gradient direction
                steps = {}
                for param_name in grads:
                    steps[param_name] = -self.step_size * grads[param_name]
                self.graph.increment_parameters(steps)

            if epoch % print_every == 0:
                y_hat = self.predict(X, y)
                resid = y - y_hat
                train_loss = sum(resid**2) / n_instances
                print(f"Epoch {epoch}:", end=" ", flush=True)
                print(
                    f"Avg objective={epoch_obj_tot / n_instances:.4f}",
                    end=" ",
                    flush=True,
                )
                print(f"Avg training loss: {train_loss:.4f}", flush=True)

    def predict(self, X, y=None):
        try:
            getattr(self, "graph")
        except AttributeError:
            raise NotFittedError(
                f"This {self.__class__.__name__} instance is not fitted yet. "
                "Call 'fit' with appropriate arguments before using this method."
            )
        n_instances = X.shape[0]
        preds = np.zeros(n_instances)
        for j in range(n_instances):
            preds[j] = self.graph.get_prediction(input_values={"x": X[j]})

        return preds


def main():
    lasso_data_fname = "lasso_data.pkl"
    (
        x_train,
        y_train,
        x_val,
        y_val,
        target_fn,
        coefs_true,
        featurize,
    ) = setup_problem.load_problem(lasso_data_fname)

    # Generate features
    X_train = featurize(x_train)
    X_val = featurize(x_val)

    pred_fns = []
    x = np.sort(np.concatenate([np.arange(0, 1, 0.001), x_train]))
    X = featurize(x)

    l2reg = 1
    estimator = RidgeRegression(l2_reg=l2reg, step_size=0.00005, max_num_epochs=2000)
    estimator.fit(X_train, y_train, print_every=100)
    name = "Ridge with L2Reg=" + str(l2reg)
    pred_fns.append({"name": name, "preds": estimator.predict(X)})

    l2reg = 0
    estimator = RidgeRegression(l2_reg=l2reg, step_size=0.0005, max_num_epochs=500)
    estimator.fit(X_train, y_train, print_every=100)
    name = f"Ridge with L2Reg={l2reg}"
    pred_fns.append({"name": name, "preds": estimator.predict(X)})

    # Let's plot prediction functions and compare coefficients for several fits
    # and the target function.

    pred_fns.append(
        {
            "name": "Target Parameter Values (i.e. Bayes Optimal)",
            "coefs": coefs_true,
            "preds": target_fn(x),
        }
    )

    plot_utils.plot_prediction_functions(
        x, pred_fns, x_train, y_train, legend_loc="best"
    )
    os.makedirs("img", exist_ok=True)
    plt.savefig(os.path.join("img", "ridge_regression.png"))
    plt.show()


if __name__ == "__main__":
    main()
