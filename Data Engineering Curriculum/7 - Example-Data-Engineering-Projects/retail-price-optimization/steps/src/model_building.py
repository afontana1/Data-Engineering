from abc import ABC, abstractmethod
from typing import List, Tuple

import lxml
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
from numpy import sqrt
from scipy.stats import shapiro
from sklearn.dummy import DummyRegressor
from sklearn.metrics import make_scorer, mean_squared_error
from sklearn.model_selection import KFold, cross_val_score, train_test_split
from statsmodels.formula.api import ols
from statsmodels.graphics.gofplots import qqplot
from statsmodels.stats.outliers_influence import variance_inflation_factor


class DataSplitter:
    """A class used to split data into training and testing parts"""

    def __init__(
        self, df: pd.DataFrame, features: List[str], target: str, test_size: float = 0.2
    ):
        """
        Args:
        df: pandas DataFrame, the entire dataset.
        features: list of str, the column names to be used as features.
        target: str, the column name to be used as target.
        test_size: float, proportion of the dataset to include in the test split.
        """
        self.df = df
        self.features = features
        self.target = target
        self.test_size = test_size

    def split(self) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
        """Splits data into training and testing parts.

        Returns:
        Tuple of pandas DataFrame and Series: (X_train, X_test, y_train, y_test)
        """
        # drop month_year and id columns
        X = self.df[self.features]
        y = self.df[self.target]
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=self.test_size, shuffle=False
        )
        return X_train, X_test, y_train, y_test


# class LinearRegressionModel:
#     """A class used to train a linear regression model"""

#     def __init__(self, X_train: pd.DataFrame, y_train: pd.Series):
#         """
#         Args:
#         X_train: pandas DataFrame, the training features.
#         y_train: pandas Series, the training target.
#         """
#         self.X_train = X_train
#         self.y_train = y_train

#     def train(self):
#         """Trains a linear regression model using statsmodels.

#         Returns:
#         statsmodels.regression.linear_model.RegressionResultsWrapper: the trained model
#         """
#         X_train = sm.add_constant(self.X_train)  # Adding a constant (intercept term) to the model
#         print(X_train)

#         model = sm.OLS(self.y_train, X_train)
#         results = model.fit()
#         print(results.summary())
#         return results

# class ModelRefinement:

#     def __init__(self, model, data):
#         self.model = model
#         self.data = data
#         self.predictors = [x for x in self.model.model.exog_names if x != 'const']
#         self.target = self.model.model.endog_names


#     def remove_insignificant_vars(self, alpha=0.05):
#         summary = self.model.summary().tables[1]
#         summary_df = pd.DataFrame(summary.data)
#         summary_df.columns = summary_df.iloc[0]
#         summary_df = summary_df.drop(0)
#         summary_df = summary_df.set_index(summary_df.columns[0])
#         summary_df['P>|t|'] = summary_df['P>|t|'].astype(float)
#         significant_vars = [var for var in self.predictors if summary_df.loc[var, 'P>|t|'] < alpha]
#         self.predictors = significant_vars
#         return significant_vars  # Added this line


#     def check_multicollinearity(self):
#         exog = sm.add_constant(self.data[self.predictors])
#         vif = pd.Series([variance_inflation_factor(exog.values, i)
#                          for i in range(exog.shape[1])],
#                         index=exog.columns)
#         print("Variance Inflation Factors:")
#         print(vif)

#     def check_normality_of_residuals(self):
#         residuals = self.model.resid
#         qqplot(residuals, line='s')
#         plt.show()
#         stat, p = shapiro(residuals)
#         print('Statistics=%.3f, p=%.3f' % (stat, p))
#         alpha = 0.05
#         if p > alpha:
#             print('Sample looks Gaussian (fail to reject H0)')
#         else:
#             print('Sample does not look Gaussian (reject H0)')

#     def check_homoscedasticity(self):
#         residuals = self.model.resid
#         plt.scatter(self.model.predict(), residuals)
#         plt.xlabel('Predicted')
#         plt.ylabel('Residual')
#         plt.axhline(y=0, color='red')
#         plt.title('Residual vs. Predicted')
#         plt.show()

#     def validate(self, k=10):
#         kf = KFold(n_splits=k)
#         y = self.data["qty"]
#         X = sm.add_constant(self.data[self.predictors])
#         errors = []

#         for train, test in kf.split(X):
#             model = sm.OLS(y.iloc[train], X.iloc[train]).fit()
#             predictions = model.predict(X.iloc[test])
#             mse = mean_squared_error(y.iloc[test], predictions)
#             errors.append(mse)
#             # print error at each fold
#             print(f"MSE: {mse}")

#         rmse = np.sqrt(np.mean(errors))
#         self.rmse = rmse
#         return rmse


# class BaselineModel:
#     def __init__(self, X, y):
#         self.X = X
#         self.y = y
#         self.model = DummyRegressor(strategy='mean')

#     def train(self):
#         self.model.fit(self.X, self.y)

#     def validate(self, k=10):
#         mse_scorer = make_scorer(mean_squared_error)
#         mse_scores = cross_val_score(self.model, self.X, self.y, cv=k, scoring=mse_scorer)
#         rmse_scores = sqrt(mse_scores)
#         print(f"Baseline MSE: {mse_scores.mean()}")
#         print(f"Baseline RMSE: {rmse_scores.mean()}")


# class InteractionEffects:

#     def __init__(self, data: pd.DataFrame):
#         """
#         Args:
#         data: pandas DataFrame, the data which might contain interacting variables.
#         """
#         self.data = data.copy()

#     def add_interaction(self, var1: str, var2: str):
#         """Adds an interaction term to the data.

#         Args:
#         var1: str, name of the first interacting variable
#         var2: str, name of the second interacting variable

#         Returns:
#         pandas DataFrame, the data with the added interaction term.
#         """
#         interaction_term = self.data[var1] * self.data[var2]
#         self.data[f'{var1}:{var2}'] = interaction_term

#     def get_data(self):
#         """Returns the data with interaction terms.

#         Returns:
#         pandas DataFrame, the data with the added interaction terms.
#         """
#         return self.data


class Model(ABC):
    """Abstract class for models."""

    @abstractmethod
    def train(self):
        """Trains the model."""
        pass

    @abstractmethod
    def validate(self, k: int):
        """Validates the model."""
        pass


class LinearRegressionModel(Model):
    """Linear regression model."""

    def __init__(self, X_train: pd.DataFrame, y_train: pd.Series):
        """
        Args:
        X_train: pandas DataFrame, the training features.
        y_train: pandas Series, the training target.
        """
        self.X_train = X_train
        self.y_train = y_train
        self.model = None

    def train(self):
        """Trains a linear regression model using statsmodels."""
        X_train = sm.add_constant(
            self.X_train
        )  # Adding a constant (intercept term) to the model
        self.model = sm.OLS(self.y_train, X_train).fit()
        print(self.model.summary())
        return self.model

    def validate(self, k=10):
        """Validates the model."""
        raise NotImplementedError(
            "Validation not implemented for linear regression model yet."
        )


class BaselineModel(Model):
    """Baseline model."""

    def __init__(self, X_train: pd.DataFrame, y_train: pd.Series):
        self.X_train = X_train
        self.y_train = y_train
        self.model = DummyRegressor(strategy="mean")

    def train(self):
        """Trains the baseline model."""
        self.model.fit(self.X_train, self.y_train)

    def validate(self, k=10):
        """Validates the baseline model."""
        mse_scorer = make_scorer(mean_squared_error)
        mse_scores = cross_val_score(
            self.model, self.X_train, self.y_train, cv=k, scoring=mse_scorer
        )
        rmse_scores = sqrt(mse_scores)
        print(f"Baseline MSE: {mse_scores.mean()}")
        print(f"Baseline RMSE: {rmse_scores.mean()}")


class ModelFactory:
    """Model factory class."""

    @staticmethod
    def get_model(model_type: str, *args, **kwargs) -> Model:
        """Get the model of the given type."""
        if model_type == "linear_regression":
            return LinearRegressionModel(*args, **kwargs)
        elif model_type == "baseline":
            return BaselineModel(*args, **kwargs)
        else:
            raise ValueError(f"Unknown model type: {model_type}")


class ModelRefinement:
    """Singleton class for refining a given model."""

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ModelRefinement, cls).__new__(cls)
        return cls._instance

    def __init__(self, model, data):
        self.model = model
        self.data = data
        self.predictors = [x for x in self.model.model.exog_names if x != "const"]
        self.target = self.model.model.endog_names
        self.rmse = None

    def remove_insignificant_vars(self, alpha=0.05):
        """Remove insignificant variables based on p-value."""
        summary = self.model.summary().tables[1]
        summary_df = pd.DataFrame(summary.data)
        summary_df.columns = summary_df.iloc[0]
        summary_df = summary_df.drop(0)
        summary_df = summary_df.set_index(summary_df.columns[0])
        summary_df["P>|t|"] = summary_df["P>|t|"].astype(float)
        significant_vars = [
            var for var in self.predictors if summary_df.loc[var, "P>|t|"] < alpha
        ]
        self.predictors = significant_vars
        return significant_vars

    def check_multicollinearity(self):
        """Check multicollinearity among predictors."""
        exog = sm.add_constant(self.data[self.predictors])
        vif = pd.Series(
            [variance_inflation_factor(exog.values, i) for i in range(exog.shape[1])],
            index=exog.columns,
        )
        print("Variance Inflation Factors:")
        print(vif)

    def check_normality_of_residuals(self):
        """Check normality of residuals."""
        residuals = self.model.resid
        qqplot(residuals, line="s")
        plt.show()
        stat, p = shapiro(residuals)
        print("Statistics=%.3f, p=%.3f" % (stat, p))
        alpha = 0.05
        if p > alpha:
            print("Sample looks Gaussian (fail to reject H0)")
        else:
            print("Sample does not look Gaussian (reject H0)")

    def check_homoscedasticity(self):
        """Check homoscedasticity."""
        residuals = self.model.resid
        plt.scatter(self.model.predict(), residuals)
        plt.xlabel("Predicted")
        plt.ylabel("Residual")
        plt.axhline(y=0, color="red")
        plt.title("Residual vs. Predicted")
        plt.show()

    def validate(self, k=10):
        """Validate the model using K-Fold cross-validation."""
        kf = KFold(n_splits=k)
        y = self.data[self.target]
        X = sm.add_constant(self.data[self.predictors])
        errors = []

        for train, test in kf.split(X):
            model = sm.OLS(y.iloc[train], X.iloc[train]).fit()
            predictions = model.predict(X.iloc[test])
            mse = mean_squared_error(y.iloc[test], predictions)
            errors.append(mse)
            print(f"MSE: {mse}")

        rmse = np.sqrt(np.mean(errors))
        self.rmse = rmse
        return rmse


if __name__ == "__main__":
    # df = pd.read_csv("/Users/ayushsingh/Desktop/MLProjectPackages/retail-price-optimization/data/retail_prices_encoded_date.csv")
    # df.drop(["month_year", "id"], axis=1, inplace=True)
    # X = df.drop(["qty"], axis=1)
    # y = df["qty"]
    # data_splitter = DataSplitter(df, X.columns, y.name)
    # X_train, X_test, y_train, y_test = data_splitter.split()
    # model = LinearRegressionModel(X_train, y_train)
    # results = model.train()
    # print(results.summary())
    # refinement1 = ModelRefinement(results, df)
    # predictors = refinement1.remove_insignificant_vars(alpha=0.05)  # removes insignificant variables
    # print(predictors)
    # X_train_significant = X_train[predictors]
    # lr_model_2 = LinearRegressionModel(X_train_significant, y_train)
    # df_with_sig_vars = pd.concat([X_train_significant, y_train], axis=1)
    # df_with_sig_vars.to_csv("/Users/ayushsingh/Desktop/MLProjectPackages/retail-price-optimization/data/retail_prices_encoded_date_sig_vars.csv", index=False)
    # model = lr_model_2.train()
    # print(model.summary())

    # refinement = ModelRefinement(model, df)

    # # Now you can use the methods defined in the class
    # # predictors = refinement.remove_insignificant_vars(alpha=0.05)  # removes insignificant variables
    # refinement.check_multicollinearity()  # checks multicollinearity among predictors
    # refinement.check_normality_of_residuals()  # checks if residuals are normally distributed
    # refinement.check_homoscedasticity()  # checks if residuals have constant variance
    # refinement.validate(k=10)  # cross-validates the model using k-fold cross-validation

    # # Assume target_var is the name of your target variable
    # target_var = 'qty'

    # # Calculate the target variable's standard deviation, mean and median
    # std_dev = np.std(refinement.data[target_var])
    # mean_value = np.mean(refinement.data[target_var])
    # median_value = np.median(refinement.data[target_var])

    # # Print the comparison
    # print(f"Standard Deviation of {target_var}: {std_dev}")
    # print(f"Mean of {target_var}: {mean_value}")
    # print(f"Median of {target_var}: {median_value}")
    # print(f"RMSE of the model: {refinement.rmse}")

    # baseline = BaselineModel(X, y)
    # baseline.train()
    # baseline.validate(k=10)

    # # Initialize the class
    # interaction_effects = InteractionEffects(df)

    # # Add interaction terms
    # interaction_effects.add_interaction('var1', 'var2')  # replace 'var1' and 'var2' with the names of your interacting variables

    # # Get the data with interaction terms
    # df_with_interaction = interaction_effects.get_data()
    pass
