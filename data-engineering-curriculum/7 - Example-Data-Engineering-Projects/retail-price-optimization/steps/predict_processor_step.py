import numpy as np  # type: ignore [import]
import pandas as pd
from zenml import step
from zenml.steps import Output


@step
def predict_preprocessor(
    X_test: pd.DataFrame, y_test: pd.Series
) -> Output(data=np.ndarray):
    """Preprocesses data for prediction."""
    combined = pd.concat([X_test, y_test], axis=1)
    combined.rename(columns={"series": "qty"}, inplace=True)
    # convert df to number array
    data = combined.to_numpy()
    return data
