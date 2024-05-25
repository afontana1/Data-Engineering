from typing import List

import pandas as pd
import statsmodels.api as sm
from statsmodels.regression.linear_model import RegressionResultsWrapper
from typing_extensions import Annotated
from zenml import step
from zenml.logger import get_logger

from steps.src.model_building import ModelRefinement

logger = get_logger(__name__)
import mlflow
from zenml.client import Client
from zenml.integrations.mlflow.experiment_trackers import MLFlowExperimentTracker

experiment_tracker = Client().active_stack.experiment_tracker

if not experiment_tracker or not isinstance(
    experiment_tracker, MLFlowExperimentTracker
):
    raise RuntimeError(
        "Your active stack needs to contain a MLFlow experiment tracker for "
        "this example to work."
    )


@step(experiment_tracker=experiment_tracker.name)
def evaluate(
    model: RegressionResultsWrapper,
    df: pd.DataFrame,
) -> Annotated[float, "rmse"]:
    """Validates the model"""

    try:
        refinement1 = ModelRefinement(model, df)
        rmse = refinement1.validate()  # removes insignificant variables
        logger.info(rmse)
        logger.info("Model Evaluated successfully")
        mlflow.log_metric("rmse", rmse)
        return rmse
    except Exception as e:
        logger.error(e)
        raise e
