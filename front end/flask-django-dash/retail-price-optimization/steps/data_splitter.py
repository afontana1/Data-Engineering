from zenml.logger import get_logger

logger = get_logger(__name__)

from typing import List, Tuple

import pandas as pd
from typing_extensions import (
    Annotated,  # or `from typing import Annotated on Python 3.9+
)
from zenml import step

from steps.src.model_building import DataSplitter


@step
def split_data(
    df: pd.DataFrame,
) -> Tuple[
    Annotated[pd.DataFrame, "X_train"],
    Annotated[pd.DataFrame, "X_test"],
    Annotated[pd.Series, "y_train"],
    Annotated[pd.Series, "y_test"],
]:
    """Splits data into training and testing parts."""
    try:
        data_splitter = DataSplitter(
            df, features=df.drop("qty", axis=1).columns, target="qty"
        )
        X_train, X_test, y_train, y_test = data_splitter.split()
        logger.info("Data split successfully")
        return X_train, X_test, y_train, y_test
    except Exception as e:
        logger.error(e)
        raise e


@step
def combine_data(
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
    y_train: pd.Series,
    y_test: pd.Series,
) -> Tuple[Annotated[pd.DataFrame, "df_train"], Annotated[pd.DataFrame, "df_test"],]:
    try:
        df_train = pd.concat([X_train, y_train], axis=1)
        df_test = pd.concat([X_test, y_test], axis=1)
        # rename series column name to qty

        df_train.rename(columns={"series": "qty"}, inplace=True)
        df_test.rename(columns={"series": "qty"}, inplace=True)

        logger.info("Data combined successfully")
        print(df_train.columns)
        print(df_test.columns)
        return df_train, df_test
    except Exception as e:
        logger.error(e)
        raise e
