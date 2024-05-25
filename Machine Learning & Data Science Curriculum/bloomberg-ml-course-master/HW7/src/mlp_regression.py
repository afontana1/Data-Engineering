import os
import matplotlib.pyplot as plt
from sklearn.base import BaseEstimator, RegressorMixin
import numpy as np
import setup_problem, nodes, graph, plot_utils


class MLPRegression(BaseEstimator, RegressorMixin):
    """MLP regression with computation graph"""

    def __init__(
        self,
        n_hidden_units=10,
        l2_reg=0,
        step_size=0.005,
        init_param_scale=0.01,
        max_num_epochs=5000,
    ):
        self.n_hidden_units = n_hidden_units
        self.init_param_scale = 0.01
        self.max_num_epochs = max_num_epochs
        self.step_size = step_size
        self.l2_reg = l2_reg

        # Build computation graph
        self.x = nodes.ValueNode(node_name="x")  # to hold a vector input
        self.y = nodes.ValueNode(node_name="y")  # to hold a scalar response
        self.W1 = nodes.ValueNode(node_name="W1")  # to hold the parameter matrix
        self.W2 = nodes.ValueNode(node_name="W2")  # to hold the parameter vector
        self.b1 = nodes.ValueNode(node_name="b1")  # to hold the bias parameter (vector)
        self.b2 = nodes.ValueNode(node_name="b2")  # to hold the bias parameter (scalar)

        f1 = nodes.AffineNode(x=self.x, W=self.W1, b=self.b1, node_name="Hidden Layer")
        a1 = nodes.TanhNode(a=f1, node_name="Hidden Activation")
        self.prediction = nodes.VectorScalarAffineNode(
            x=a1, w=self.W2, b=self.b2, node_name="Output"
        )

        data_loss = nodes.SquaredL2DistanceNode(
            a=self.prediction, b=self.y, node_name="Data Loss"
        )
        reg_loss1 = nodes.L2NormPenaltyNode(
            l2_reg=self.l2_reg, w=self.W1, node_name="W1 Decay"
        )
        reg_loss2 = nodes.L2NormPenaltyNode(
            l2_reg=self.l2_reg, w=self.W2, node_name="W2 Decay"
        )
        total_reg_loss = nodes.SumNode(
            a=reg_loss1, b=reg_loss2, node_name="Regularization Loss"
        )

        self.objective = nodes.SumNode(
            a=data_loss, b=total_reg_loss, node_name="Total Loss"
        )

        self.inputs = [self.x]
        self.outcomes = [self.y]
        self.parameters = [self.W1, self.W2, self.b1, self.b2]

        self.graph = graph.ComputationGraphFunction(
            self.inputs, self.outcomes, self.parameters, self.prediction, self.objective
        )

    def fit(self, X, y, print_every=50):
        n_instances, n_ftrs = X.shape
        y = y.reshape(-1)

        s = self.init_param_scale
        init_values = {
            "W1": s * np.random.normal(size=(self.n_hidden_units, n_ftrs)),
            "b1": s * np.random.normal(size=(self.n_hidden_units)),
            "W2": s * np.random.normal(size=(self.n_hidden_units)),
            "b2": s * np.array(np.random.randn()),
        }

        self.graph.set_parameters(init_values)

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
                train_loss = sum((y - self.predict(X, y)) ** 2) / n_instances
                print(f"Epoch {epoch}:", end=" ", flush=True)
                print(
                    f"Avg objective={epoch_obj_tot / n_instances:.4f}",
                    end=" ",
                    flush=True,
                )
                print(f"Avg training loss {train_loss:.4f}", flush=True)

    def predict(self, X, y=None):
        try:
            getattr(self, "graph")
        except AttributeError:
            raise RuntimeError("You must train classifer before predicting data!")

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

    # Let's plot prediction functions and compare coefficients for several fits
    # and the target function.
    pred_fns = []
    x = np.sort(np.concatenate([np.arange(0, 1, 0.001), x_train]))

    pred_fns.append(
        {
            "name": "Target Parameter Values (i.e. Bayes Optimal)",
            "coefs": coefs_true,
            "preds": target_fn(x),
        }
    )

    estimator = MLPRegression(
        n_hidden_units=10,
        step_size=0.001,
        init_param_scale=0.0005,
        max_num_epochs=5000,
        l2_reg=0.001,
    )

    # fit expects a 2-dim array
    x_train_as_column_vector = x_train.reshape(x_train.shape[0], 1)
    x_as_column_vector = x.reshape(x.shape[0], 1)  # fit expects a 2-dim array
    estimator.fit(x_train_as_column_vector, y_train, print_every=100)
    name = "MLP regression - no features"
    pred_fns.append({"name": name, "preds": estimator.predict(x_as_column_vector)})

    X = featurize(x)
    estimator = MLPRegression(
        n_hidden_units=10,
        step_size=0.0005,
        init_param_scale=0.01,
        max_num_epochs=500,
        l2_reg=0.001,
    )
    estimator.fit(X_train, y_train)
    name = "MLP regression - with features"
    pred_fns.append({"name": name, "preds": estimator.predict(X)})
    plot_utils.plot_prediction_functions(
        x, pred_fns, x_train, y_train, legend_loc="best"
    )

    os.makedirs("img", exist_ok=True)
    plt.savefig(os.path.join("img", "mlp_regression.png"))
    plt.show()


if __name__ == "__main__":
    main()
