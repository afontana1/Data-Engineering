from typing import List

import statsmodels.api as sm
from scipy.stats import shapiro
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import KFold
from statsmodels.stats.outliers_influence import variance_inflation_factor
from zenml.logger import get_logger

logger = get_logger(__name__)

import pandas as pd
from statsmodels.regression.linear_model import RegressionResultsWrapper
from typing_extensions import Annotated
from zenml import step

from materializer.custom_materializer import StatsModelMaterializer
from steps.src.model_building import LinearRegressionModel, ModelRefinement


@step()
def remove_insignificant_vars(
    model: RegressionResultsWrapper,
    df: pd.DataFrame,
    alpha: float = 0.05,
) -> Annotated[List[str], "significant_predictors"]:
    """Removes insignificant predictors from the model."""

    try:
        # predictors = [x for x in model.model.exog_names if x != 'const']
        # target = model.model.endog_names
        print(type(model))
        print(model.summary())
        refinement1 = ModelRefinement(model, df)
        predictors = refinement1.remove_insignificant_vars(
            alpha=alpha
        )  # removes insignificant variables
        logger.info("Model refined successfully")
        return predictors
    except Exception as e:
        logger.error(e)
        raise e
