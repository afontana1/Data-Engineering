import time

import pandas as pd
from sqlalchemy import create_engine, exc


class DataLoader:
    """
    DataLoader class encapsulates the details of connecting to a database
    and loading data into a pandas DataFrame.
    """

    def __init__(self, db_uri: str):
        """
        Initializes DataLoader class with a database URI and creates an SQLAlchemy engine.

        Args:
            db_uri (str): The database URI.
        """
        self.db_uri = db_uri
        self.engine = create_engine(self.db_uri)
        self.data = None

    def timed(func):
        """
        Decorator function to measure the execution time of the function it decorates.

        Args:
            func (callable): The function to be decorated.

        Returns:
            callable: The decorated function.
        """

        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            print(f"'{func.__name__}' function executed in {end - start}s")
            return result

        return wrapper

    @timed
    def load_data(self, table_name: str) -> pd.DataFrame:
        """
        Loads data from the specified table into a DataFrame, which is stored
        as an instance variable self.data.

        Args:
            table_name (str): The name of the table from which to load data.

        Returns:
            pd.DataFrame: The loaded data.

        Raises:
            ValueError: If the table does not exist or the query execution fails.
        """
        query = "SELECT * FROM " + table_name
        try:
            self.data = pd.read_sql_query(query, self.engine)
            return self.data
        except exc.SQLAlchemyError as e:
            raise ValueError(f"Failed to execute query: {e}")

    def get_data(self) -> pd.DataFrame:
        """
        Returns the loaded data. If no data has been loaded, it raises a ValueError.

        Returns:
            pd.DataFrame: The loaded data.

        Raises:
            ValueError: If data has not been loaded yet.
        """
        if self.data is not None:
            return self.data
        else:
            raise ValueError(
                "Data has not been loaded yet. Please call 'load_data' first."
            )


# data_loader = DataLoader('postgresql://postgres:ayushsingh@localhost:5432/cs001')
# data_loader.load_data('retail_prices')
# df = data_loader.get_data()
# print(df.head())
