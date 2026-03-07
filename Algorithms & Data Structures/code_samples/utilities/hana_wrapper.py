from hdbcli import dbapi
import pandas as pd
import sys

from pyspark.sql import SparkSession, Row, DataFrame
from pyspark.sql.functions import udf, col, explode, substring, length
from pyspark.sql.types import (
    StructType,
    TimestampType,
    LongType,
    IntegerType,
    StringType,
    DoubleType,
    FloatType,
    StructField,
)
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ["JOB_NAME"])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)
job.commit()


class Cursor_Iterator:
    """Cursor iterator with column name"""

    def __init__(self, cursor):
        self._cursor = cursor

    def __iter__(self):
        return self

    def __next__(self):
        row = self._cursor.__next__()
        return {
            description[0]: row[col]
            for col, description in enumerate(self._cursor.description)
        }


class Hana_Connection:
    def __init__(self, server, port, user, password):
        self.server = server
        self.port = port
        self.user = user
        self.password = password
        self._conn = None
        self._cursor = None

    def __enter__(self):
        self._conn = dbapi.connect(
            address=self.server, port=self.port, user=self.user, password=self.password
        )
        self._cursor = self._conn.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._cursor.close()
        self._conn.close()

    def __iter__(self):
        return Cursor_Iterator(self._cursor)

    def execute_query(self, query):
        try:
            self._cursor.execute(query)
        except Exception as e:
            raise (e)

    def create_df_from_results(self, result_set):
        try:
            print("creating DataFrame")
            df = pd.DataFrame(result_set)
            df = df.fillna(0)
            spark_df = self.pandas_to_spark(df)
            return spark_df
        except Exception as e:
            raise (e)

    def equivalent_type(self, f):
        if f == "datetime64[ns]":
            return TimestampType()
        elif f == "int64":
            return LongType()
        elif f == "int32":
            return IntegerType()
        elif f == "float64":
            return DoubleType()
        elif f == "float32":
            return FloatType()
        else:
            return StringType()

    def define_structure(self, string, format_type):
        try:
            typo = self.equivalent_type(format_type)
        except:
            typo = StringType()
        return StructField(string, typo)

    def pandas_to_spark(self, pandas_df):
        columns = list(pandas_df.columns)
        types = list(pandas_df.dtypes)
        struct_list = []
        for column, typo in zip(columns, types):
            struct_list.append(self.define_structure(column, typo))
        p_schema = StructType(struct_list)
        return spark.createDataFrame(pandas_df, p_schema)
