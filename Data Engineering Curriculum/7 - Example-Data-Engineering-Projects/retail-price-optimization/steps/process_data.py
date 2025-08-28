from typing import Tuple

import pandas as pd
from typing_extensions import (
    Annotated,  # or `from typing import Annotated on Python 3.9+
)
from zenml import step
from zenml.logger import get_logger

from steps.src.data_processor import CategoricalEncoder, OutlierHandler
from steps.src.feature_engineering import DateFeatureEngineer

logger = get_logger(__name__)


@step
def categorical_encode(df: pd.DataFrame) -> pd.DataFrame:
    """
    Processes the data by applying categorical encoding and outlier handling.

    Args:
        df: pd.DataFrame: Input dataframe to be processed.

    Returns:
        data: pd.DataFrame: Processed dataframe.
    """
    try:
        # Apply categorical encoding
        print(df.head())
        encoder = CategoricalEncoder(method="onehot")
        df = encoder.fit_transform(df, columns=["product_id", "product_category_name"])

        # Handle outliers
        outlier_handler = OutlierHandler(multiplier=1.5)
        df_transformed = outlier_handler.fit_transform(
            df, columns=["total_price", "freight_price", "unit_price"]
        )

        logger.info("Data processed successfully")
        return df_transformed

    except Exception as e:
        logger.error(e)
        raise e


@step
def feature_engineer(df: pd.DataFrame) -> pd.DataFrame:
    """
    Performs feature engineering on the data.

    Args:
        df (pd.DataFrame): Input DataFrame to be processed.

    Returns:
        pd.DataFrame: DataFrame after feature engineering.
    """
    try:
        # Apply date feature engineering
        date_engineer = DateFeatureEngineer(date_format="%Y-%m-%d")
        df_transformed = date_engineer.fit_transform(df, ["month_year"])

        # Log the successful operation
        logger.info("Feature engineering applied successfully")

        # Drop unnecessary columns
        df_transformed.drop(["id", "month_year"], axis=1, inplace=True)

        return df_transformed

    except Exception as e:
        logger.error(e)
        raise e
