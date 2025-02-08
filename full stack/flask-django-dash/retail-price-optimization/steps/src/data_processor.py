from abc import ABC, abstractmethod
from typing import List

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder

from steps.src.data_loader import DataLoader


class CategoricalEncoder:
    """
    This class applies encoding to categorical variables.

    Parameters
    ----------
    method: str, default="onehot"
        The method to encode the categorical variables. Can be "onehot" or "ordinal".

    categories: 'auto' or a list of lists, default='auto'
        Categories for the encoders. Must match the number of columns. If 'auto', categories are determined from data.
    """

    def __init__(self, method="onehot", categories="auto"):
        self.method = method
        self.categories = categories
        self.encoders = {}

    def fit(self, df, columns):
        """
        This function fits the encoding method to the provided data.

        Parameters
        ----------
        df: pandas DataFrame
            The input data to fit.

        columns: list of str
            The names of the columns to encode.
        """
        for col in columns:
            if self.method == "onehot":
                self.encoders[col] = OneHotEncoder(
                    sparse=False, categories=self.categories
                )
            elif self.method == "ordinal":
                self.encoders[col] = OrdinalEncoder(categories=self.categories)
            else:
                raise ValueError(f"Invalid method: {self.method}")
            # Encoders expect 2D input data
            self.encoders[col].fit(df[[col]])

    def transform(self, df, columns):
        """
        This function applies the encoding to the provided data.

        Parameters
        ----------
        df: pandas DataFrame
            The input data to transform.

        columns: list of str
            The names of the columns to encode.
        """
        df_encoded = df.copy()
        for col in columns:
            # Encoders expect 2D input data
            transformed = self.encoders[col].transform(df[[col]])
            if self.method == "onehot":
                # OneHotEncoder returns a 2D array, we need to convert it to a DataFrame
                transformed = pd.DataFrame(
                    transformed, columns=self.encoders[col].get_feature_names_out([col])
                )
                df_encoded = pd.concat(
                    [df_encoded.drop(columns=[col]), transformed], axis=1
                )
            else:
                df_encoded[col] = transformed
        return df_encoded

    def fit_transform(self, df, columns):
        """
        This function fits the encoding method to the provided data and then transforms the data.

        Parameters
        ----------
        df: pandas DataFrame
            The input data to fit and transform.

        columns: list of str
            The names of the columns to encode.
        """
        self.fit(df, columns)
        return self.transform(df, columns)


# class Encoder(ABC):
#     """
#     The Encoder interface declares operations common to all supported encoding algorithms.

#     Methods:
#         fit(self, df: pd.DataFrame, col: str)
#             Fits the encoder using the provided DataFrame and column.

#         transform(self, df: pd.DataFrame, col: str) -> pd.DataFrame
#             Transforms the DataFrame using the fitted encoder and returns the transformed DataFrame.
#     """

#     @abstractmethod
#     def fit(self, df: pd.DataFrame, col: str):
#         """
#         Fits the encoder using the provided DataFrame and column.

#         Parameters:
#             df (pd.DataFrame): DataFrame to fit the encoder on.
#             col (str): Column to fit the encoder on.
#         """
#         pass

#     @abstractmethod
#     def transform(self, df: pd.DataFrame, col: str) -> pd.DataFrame:
#         """
#         Transforms the DataFrame using the fitted encoder and returns the transformed DataFrame.

#         Parameters:
#             df (pd.DataFrame): DataFrame to transform.
#             col (str): Column to transform.

#         Returns:
#             df (pd.DataFrame): Transformed DataFrame.
#         """
#         pass


# class OneHotEncoderStrategy(Encoder):
#     """
#     Concrete OneHotEncoderStrategy class implementing the Encoder interface.

#     Attributes:
#         encoder (OneHotEncoder): Instance of OneHotEncoder from sklearn.

#     Methods:
#         fit(self, df: pd.DataFrame, col: str)
#             Fits the OneHotEncoder using the provided DataFrame and column.

#         transform(self, df: pd.DataFrame, col: str) -> pd.DataFrame
#             Transforms the DataFrame using the fitted OneHotEncoder and returns the transformed DataFrame.
#     """

#     def __init__(self, categories):
#         self.encoder = OneHotEncoder(sparse=False, categories=categories)

#     def fit(self, df: pd.DataFrame, col: str):
#         self.encoder.fit(df[[col]])

#     def transform(self, df: pd.DataFrame, col: str) -> pd.DataFrame:
#         transformed = self.encoder.transform(df[[col]])
#         transformed = pd.DataFrame(transformed, columns=self.encoder.get_feature_names_out([col]))
#         return pd.concat([df.drop(columns=[col]), transformed], axis=1)


# class OrdinalEncoderStrategy(Encoder):
#     """
#     Concrete OrdinalEncoderStrategy class implementing the Encoder interface.

#     Attributes:
#         encoder (OrdinalEncoder): Instance of OrdinalEncoder from sklearn.

#     Methods:
#         fit(self, df: pd.DataFrame, col: str)
#             Fits the OrdinalEncoder using the provided DataFrame and column.

#         transform(self, df: pd.DataFrame, col: str) -> pd.DataFrame
#             Transforms the DataFrame using the fitted OrdinalEncoder and returns the transformed DataFrame.
#     """

#     def __init__(self, categories):
#         self.encoder = OrdinalEncoder(categories=categories)

#     def fit(self, df: pd.DataFrame, col: str):
#         self.encoder.fit(df[[col]])

#     def transform(self, df: pd.DataFrame, col: str) -> pd.DataFrame:
#         df[col] = self.encoder.transform(df[[col]])
#         return df


# class CategoricalEncoder:
#     """
#     The CategoricalEncoder class uses an Encoder strategy to perform encoding.

#     Attributes:
#         strategy (Encoder): Instance of Encoder (OneHotEncoderStrategy or OrdinalEncoderStrategy).
#         encoders (dict): Empty dictionary to store fitted encoders.

#     Methods:
#         fit(self, df: pd.DataFrame, columns: List[str])
#             Fits the encoder strategy using the provided DataFrame and columns.

#         transform(self, df: pd.DataFrame, columns: List[str]) -> pd.DataFrame
#             Transforms the DataFrame using the fitted encoder strategy and returns the transformed DataFrame.

#         fit_transform(self, df: pd.DataFrame, columns: List[str]) -> pd.DataFrame
#             Fits the encoder strategy and then transforms the DataFrame, returns the transformed DataFrame.
#     """

#     def __init__(self, method="onehot", categories='auto'):
#         if method == "onehot":
#             self.strategy = OneHotEncoderStrategy(categories)
#         elif method == "ordinal":
#             self.strategy = OrdinalEncoderStrategy(categories)
#         else:
#             raise ValueError(f"Invalid method: {method}")
#         self.encoders = {}

#     def fit(self, df: pd.DataFrame, columns: List[str]):
#         for col in columns:
#             self.strategy.fit(df, col)

#     def transform(self, df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
#         df_encoded = df.copy()
#         for col in columns:
#             df_encoded = self.strategy.transform(df_encoded, col)
#         return df_encoded

#     def fit_transform(self, df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
#         self.fit(df, columns)
#         return self.transform(df, columns)


class OutlierHandler:
    """
    A class used to handle outliers in a pandas DataFrame.

    ...

    Attributes
    ----------
    multiplier : float
        The multiplier for the IQR. Observations outside of the range [Q1 - multiplier*IQR, Q3 + multiplier*IQR] are considered outliers.

    Methods
    -------
    fit(df: pd.DataFrame, columns: List[str])
        Compute the median and IQR for each specified column in the DataFrame.
    transform(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame
        Replace outliers in the specified columns with the respective column's median.
    fit_transform(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame
        Fit the OutlierHandler to the DataFrame and then transform the DataFrame.
    """

    def __init__(self, multiplier: float = 1.5):
        """
        Constructs all the necessary attributes for the OutlierHandler object.

        Parameters
        ----------
            multiplier : float
                The multiplier for the IQR. Observations outside of the range [Q1 - multiplier*IQR, Q3 + multiplier*IQR] are considered outliers.
        """
        self.multiplier = multiplier
        self.medians = {}
        self.iqr_bounds = {}
        self.outliers = pd.DataFrame()

    def fit(self, df: pd.DataFrame, columns: List[str]):
        """
        Compute the median and IQR for each specified column in the DataFrame.

        Parameters
        ----------
            df : pd.DataFrame
                The DataFrame to compute the median and IQR on.
            columns : List[str]
                The columns of the DataFrame to compute the median and IQR on.
        """
        for col in columns:
            self.medians[col] = df[col].median()
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            self.iqr_bounds[col] = (
                Q1 - self.multiplier * IQR,
                Q3 + self.multiplier * IQR,
            )

    def transform(self, df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
        """
        Replace outliers in the specified columns with the respective column's median.

        Parameters
        ----------
            df : pd.DataFrame
                The DataFrame to replace outliers in.
            columns : List[str]
                The columns of the DataFrame to replace outliers in.

        Returns
        -------
            df : pd.DataFrame
                The DataFrame with outliers replaced.
        """
        for col in columns:
            outliers = df[
                (df[col] < self.iqr_bounds[col][0])
                | (df[col] > self.iqr_bounds[col][1])
            ]
            self.outliers = pd.concat([self.outliers, outliers])
            df[col] = np.where(
                (df[col] < self.iqr_bounds[col][0])
                | (df[col] > self.iqr_bounds[col][1]),
                self.medians[col],
                df[col],
            )
        return df

    def fit_transform(self, df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
        """
        Fit the OutlierHandler to the DataFrame and then transform the DataFrame.

        Parameters
        ----------
            df : pd.DataFrame
                The DataFrame to fit the OutlierHandler on and replace outliers in.
            columns : List[str]
                The columns of the DataFrame to fit the OutlierHandler on and replace outliers in.

        Returns
        -------
            df : pd.DataFrame
                The DataFrame with outliers replaced.
        """
        self.fit(df, columns)
        return self.transform(df, columns)


# data_loader = DataLoader('postgresql://postgres:ayushsingh@localhost:5432/cs001')
# data_loader.load_data('retail_prices')
# df = data_loader.get_data()
# encoder = CategoricalEncoder(method="onehot")
# df = encoder.fit_transform(df, columns=["product_id", "product_category_name"])
# df.to_csv("../data/retail_prices_encoded.csv", index=False)
# df = pd.read_csv("../data/retail_prices_encoded_date.csv")
# outlier_handler = OutlierHandler(multiplier=1.5)
# df_transformed = outlier_handler.fit_transform(df, columns=["total_price", "freight_price", "unit_price"])

# print("Transformed DataFrame:")
# print(df_transformed)

# print("\nOutliers:")
# print(outlier_handler.outliers.shape)
