from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession \
        .builder \
        .appName("ETL") \
        .config("spark.jars.packages",
        "org.apache.spark:spark-hadoop-cloud_2.12:3.3.2,postgresql:postgresql:9.1-901.jdbc4") \
        .config("spark.hadoop.fs.s3.endpoint", "s3-us-east-1.amazonaws.com") \
        .config("spark.hadoop.com.amazonaws.services.s3.enableV4", "true") \
        .config("spark.hadoop.fs.s3.impl", "org.apache.hadoop.fs.s3a.S3FileSystem") \
        .config('spark.hadoop.fs.s3a.aws.credentials.provider', 'org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider') \
        .config('spark.hadoop.fs.s3a.access.key', 'youraccesskey') \
        .config('spark.hadoop.fs.s3a.secret.key', 'yoursecretkey') \
        .config("spark.executor.memory", "6g") \
        .config("spark.executor.cores", 3) \
        .master("spark://spark-master:7077") \
        .getOrCreate()


df = spark.read.parquet('s3a://mysql-iago/taxis/green_taxi/', inferSchema=True)

df_agg = (
        df.filter(
                F.col('tolls_amount') > 0
        ).groupBy(
                F.col('DOLocationID')
        ).agg(
                F.avg('trip_distance').alias('avg_distance')
        ).orderBy('DOLocationID')
)

mode = "overwrite"
url = "jdbc:postgresql://warehouse:5432/analyst"
properties = {"user": "analyst","password": "analyst","driver": "org.postgresql.Driver"}
df_agg.write.option('truncate', 'true').jdbc(url=url, table="aggregations.tolls_avg_distance", mode='overwrite', properties=properties)