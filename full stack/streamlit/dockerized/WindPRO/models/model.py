import numpy as np
import pandas as pd
from typing import List, Tuple
import warnings

import mlflow
import mlflow.sklearn
import mlflow.pyfunc
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import KFold
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import xgboost as xgb

# Ignore all warnings
warnings.filterwarnings("ignore")

class Model():
    def __init__(self, station: str, RUN_ID: str, model_name: str, version: int) -> None:
        '''
        Initialize the Model class with station details, run ID, model name, and version.

        Args:
            station: The station for which the model is being initialized.
            RUN_ID: The run ID for tracking in MLFlow.
            model_name: The name of the model.
            version: The version of the model.
        '''
        self.station = station 
        self.id = RUN_ID 
        self.model_name = model_name
        self.version = version
        self.feature_names = ['Month', 'Hour', 'WindForecast', 'GustForecast',	
                              'WindDirForecast', 'Temperature', 'Precipitation', 'Cloudcover']   
        try:
            self._load_model()
        except Exception as e:
            print(f'Model not found initiating default model and training: {str(e)}')
            
    def transform(self, df_measurments: pd.DataFrame, df_forecast: pd.DataFrame, mode='base') -> None:
        '''
        Transform and merge measurement and forecast dataframes to prepare for training.

        Args:
            df_measurments: The dataframe containing weather measurement data.
            df_forecast: The dataframe containing forecast data.
            mode: Mode of the model, either 'base' or 'gust'. Defaults to 'base'.
        '''
        # Set the 'Time' column as the index
        df_measurments.set_index('Time', inplace=True)

        # Resample the data with a two-hour interval and apply mean aggregation
        df_measurments = df_measurments.resample('2H').mean()

        df_measurments.reset_index(inplace=True)

        df = pd.merge(left=df_forecast, right=df_measurments, on='Time', how='inner')

        df.dropna(inplace=True)

        # Close the database connections
        self.df = df
        
        # Features and labels split
        self.X = self.df[self.feature_names]
        if mode == 'base':
            self.y = self.df['WindSpeed']
        elif mode =='gust':
            self.y = self.df['WindGust']
   
    def parameter_tuning(self) -> None:
        '''Perform parameter tuning for the XGBoost model using grid search.'''
        self.k_fold = KFold(n_splits=5, shuffle=True, random_state=42)

        self.params_grid = {
         'max_depth': [2, 3],
         'learning_rate': [0.005,0.01, 0.1],
         'n_estimators': [30, 50],
            }
        
        # Grid search
        xgb_regressor = xgb.XGBRegressor()
        grid = GridSearchCV(xgb_regressor, self.params_grid, cv=self.k_fold)
        grid.fit(self.X, self.y)

        self.best_max_depth = grid.best_params_['max_depth']
        self.best_learning_rate = grid.best_params_['learning_rate']
        self.best_n_estimators = grid.best_params_['n_estimators']
        # Add other best hyperparameters as needed

        mlflow.log_param(f'best_max_depth', self.best_max_depth)
        mlflow.log_param(f'best_learning_rate', self.best_learning_rate)
        mlflow.log_param(f'best_n_estimators', self.best_n_estimators)
        mlflow.log_param(f'param_grid', self.params_grid)

        self.model = xgb.XGBRegressor(
                                    max_depth=self.best_max_depth,
                                    learning_rate=self.best_learning_rate,
                                    n_estimators=self.best_n_estimators,
                                    )
        
    def k_fold_cross_validation(self):
        # Run k-fold cross validation
        kfold_scores = cross_val_score(self.model, self.X, self.y, cv=self.k_fold)

        # Track metrics
        mlflow.log_metric(f"average_accuracy", kfold_scores.mean())
        mlflow.log_metric(f"std_accuracy", kfold_scores.std())
        return kfold_scores.mean()

    def fit(self) -> None:
        '''Train the model.'''
        self.model.fit(self.X, self.y)

    def save_model(self) -> None:
        '''Register and log the model using MLFlow.'''
        mlflow.register_model(f"runs:/{self.id}/sklearn-model", self.model_name)
        mlflow.sklearn.log_model(self.model, "sklearn-model")

    def predict(self, X: pd.DataFrame) -> List[float]:
        '''
        Make predictions using the trained model.

        Args:
            X: The input features for making predictions.

        Returns:
            A list of predictions.
        '''
        pred = self.model.predict(X)
        return pred.tolist()

    def model_evaluation(self, test_data: pd.DataFrame, mode='base') -> Tuple[float, float]:
        '''
        Evaluate the model on test data and compare with forecast data.

        Args:
            test_data: The test data for evaluation.
            mode: Mode of the model, either 'base' or 'gust'. Defaults to 'base'.

        Returns:
            A tuple containing R2 scores for model predictions and classic forecast.
        '''
        X_test = test_data[self.feature_names]
        if mode == 'base':
            y_forecast = test_data['WindForecast']
            y_test = test_data['WindSpeed']
        elif mode == 'gust':
            y_forecast = test_data['GustForecast']
            y_test = test_data['WindGust']
        y_pred = self.model.predict(X_test)
        test_data['Prediction'] = y_pred

        mlflow.log_metric(f"test_accuracy", r2_score(y_test, y_pred))
        mlflow.log_metric(f"forecast_accuracy", r2_score(y_test, y_forecast))

        mlflow.log_metric(f"test_mae", mean_absolute_error(y_test, y_pred))
        mlflow.log_metric(f"forecast_mae", mean_absolute_error(y_test, y_forecast))

        mlflow.log_metric(f"test_mse", mean_squared_error(y_test, y_pred))
        mlflow.log_metric(f"forecast_mse", mean_squared_error(y_test, y_forecast))

        mlflow.log_metric(f"test_rmse", np.sqrt(mean_squared_error(y_test, y_pred)))
        mlflow.log_metric(f"forecast_rmse", np.sqrt(mean_squared_error(y_test, y_forecast)))

        mlflow.log_param("model", mode)
        mlflow.log_param("station", self.station)
        mlflow.log_param("Date Range min", test_data['Time'].min())
        mlflow.log_param("Date Range max", test_data['Time'].max())

        return r2_score(y_test, y_pred), r2_score(y_test, y_forecast)

    def _load_model(self) -> None:
        '''Load a trained model from a pickle file.'''
        self.model = mlflow.pyfunc.load_model(model_uri=f"models:/{self.model_name}/{self.version}")
