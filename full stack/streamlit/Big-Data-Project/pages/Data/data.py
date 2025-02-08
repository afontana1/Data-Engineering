from pyspark.sql.functions import col, expr, explode, monotonically_increasing_id, sum
from pyspark.sql import SparkSession
from pyspark import SparkConf
import pandas as pd
import streamlit as st

spark = None

# Spark Session
def spark_session():
    if 'spark_initialized' not in st.session_state:
        spark = SparkSession \
            .builder \
            .appName("Streamlit-Data") \
            .master("local") \
            .config("spark.sql.warehouse.dir", "hdfs://namenode:8020/user/hive/warehouse") \
            .enableHiveSupport() \
            .getOrCreate()
        st.session_state['spark_initialized'] = True
        st.session_state['spark'] = spark

    else:
        spark = st.session_state['spark']
    return spark


#Load Business data
def business_data(spark):
    business = spark.sql("SELECT * FROM business")
    return business

# Business Attributes
def business_attributes(business):
    df_business = business
    business_attributes = df_business.select(
    col("business_id"),
    col("attributes.*"),
    )
    attributes_name = pd.DataFrame(business_attributes.columns[1:]).reset_index()
    attributes_name.rename(columns={"index": "id", 0: "name"}, inplace=True)
    
    stack_expr = "stack({}, {}) as (attribute_id, value)".format(len(business_attributes.columns[1:]), ", ".join(["'{}', {}".format(i, c) for i,c in enumerate(business_attributes.columns[1:])]))
    business_attributes = business_attributes.selectExpr("business_id", stack_expr)
    business_attributes = business_attributes.na.drop(subset="value")
    return business_attributes, attributes_name


#Spark Hours
def busines_hours(business):
    df_business = business
    business_hours = df_business.select(
    col("business_id"),
    col("hours.*"),
    )
    
    hours_name = pd.DataFrame(business_hours.columns[1:]).reset_index()
    hours_name.rename(columns={"index": "id", 0: "name"}, inplace=True)
    
    
    stack_expr = "stack({}, {}) as (day_id, open_hours)".format(len(business_hours.columns[1:]), ", ".join(["'{}', {}".format(business_hours.columns[1:][i], c) for i,c in enumerate(business_hours.columns[1:])]))
    business_hours = business_hours.selectExpr("business_id", stack_expr)
    business_hours = business_hours.na.drop(subset="open_hours")
    
    
    business_hours_df = business_hours.toPandas()
    business_hours_df[['open_hours', 'close_hours']] = business_hours_df['open_hours'].str.split('-', n=1, expand=True)
    return hours_name, business_hours_df

def business_category(business):
    df_business = business
    business_categories = df_business.select(
    col("business_id"),
    col("categories"),
    ).filter(col("categories").isNotNull() & (col("categories") != ""))
    
    # Remove space and lower text 
    business_categories = business_categories.withColumn("categories", expr("lower(trim(categories))"))
    
    # Split the categories within each row.
    business_categories = business_categories.withColumn("category_list", expr("split(categories, '\\,')"))
    
    # Explode the categories into separate individual rows.
    business_categories = business_categories.select(
        col("business_id"),
        explode(col("category_list")).alias("category")
    )
    
    # Trim Spaces the categories within each row.
    business_categories = business_categories.withColumn("category", expr("trim(category)"))
    
    # Drop duplicates
    business_categories = business_categories.dropDuplicates()
    
    # Create spark dataframes
    unique_categories = business_categories.select("category").distinct()
    
    # Creating category_id
    category_mapping = unique_categories.withColumn("category_id", monotonically_increasing_id())
    business_categories_result = business_categories.join(category_mapping, on="category").select("business_id", "category_id")
    return business_categories_result, business_categories, category_mapping





