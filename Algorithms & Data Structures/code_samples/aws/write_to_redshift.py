### READ

from pyspark.sql import SparkSession

# Create a SparkSession
spark = (
    SparkSession.builder.appName("RedshiftRead")
    .config("spark.redshift.url", "jdbc:redshift://redshift_host:port/database")
    .config("spark.redshift.user", "username")
    .config("spark.redshift.password", "password")
    .config("spark.redshift.tempdir", "s3n://temp-bucket/temp-dir")
    .config("spark.redshift.numPartitions", "10")
    .getOrCreate()
)

# Read data from Redshift table in parallel
data = (
    spark.read.format("com.databricks.spark.redshift")
    .option("url", "jdbc:redshift://redshift_host:port/database")
    .option("tempdir", "s3n://temp-bucket/temp-dir")
    .option("dbtable", "table_name")
    .option("forward_spark_s3_credentials", "true")
    .load()
)

# Show data
data.show()


### Write

from pyspark.sql import SparkSession

# Create a SparkSession
spark = (
    SparkSession.builder.appName("RedshiftWrite")
    .config("spark.redshift.url", "jdbc:redshift://redshift_host:port/database")
    .config("spark.redshift.user", "username")
    .config("spark.redshift.password", "password")
    .config("spark.redshift.tempdir", "s3n://temp-bucket/temp-dir")
    .config("spark.redshift.numPartitions", "10")
    .getOrCreate()
)

# Create a DataFrame
data = spark.createDataFrame([(1, "foo"), (2, "bar")], ["id", "name"])

# Write DataFrame to Redshift table in parallel
data.write.format("com.databricks.spark.redshift").option(
    "url", "jdbc:redshift://redshift_host:port/database"
).option("tempdir", "s3n://temp-bucket/temp-dir").option(
    "dbtable", "table_name"
).option(
    "forward_spark_s3_credentials", "true"
).mode(
    "append"
).save()


### Multiple data

from pyspark.sql import SparkSession

# Create a SparkSession
spark = (
    SparkSession.builder.appName("RedshiftMigration")
    .config("spark.redshift.url", "jdbc:redshift://src_redshift_host:port/src_database")
    .config("spark.redshift.user", "src_username")
    .config("spark.redshift.password", "src_password")
    .config("spark.redshift.tempdir", "s3n://src_temp-bucket/temp-dir")
    .config("spark.redshift.numPartitions", "10")
    .getOrCreate()
)

# List of tables to migrate
tables = ["table1", "table2", "table3"]

# Loop through tables and migrate
for table in tables:
    # Read data from Redshift table in parallel
    data = (
        spark.read.format("com.databricks.spark.redshift")
        .option("url", "jdbc:redshift://src_redshift_host:port/src_database")
        .option("tempdir", "s3n://src_temp-bucket/temp-dir")
        .option("dbtable", table)
        .option("forward_spark_s3_credentials", "true")
        .load()
    )

    # Save dataframe to destination redshift
    data.write.format("com.databricks.spark.redshift").option(
        "url", "jdbc:redshift://dest_redshift_host:port/dest_database"
    ).option("tempdir", "s3n://dest_temp-bucket/temp-dir").option(
        "dbtable", table
    ).option(
        "forward_spark_s3_credentials", "true"
    ).option(
        "extracopyoptions", "TRUNCATECOLUMNS"
    ).mode(
        "overwrite"
    ).save()


### Parallel

from pyspark.sql import SparkSession
import multiprocessing as mp

# Create a SparkSession
spark = (
    SparkSession.builder.appName("RedshiftMigration")
    .config("spark.redshift.url", "jdbc:redshift://src_redshift_host:port/src_database")
    .config("spark.redshift.user", "src_username")
    .config("spark.redshift.password", "src_password")
    .config("spark.redshift.tempdir", "s3n://src_temp-bucket/temp-dir")
    .config("spark.redshift.numPartitions", "10")
    .getOrCreate()
)

# List of tables to migrate
tables = ["table1", "table2", "table3"]

# Define a function to migrate a single table
def migrate_table(table):
    # Read data from Redshift table in parallel
    data = (
        spark.read.format("com.databricks.spark.redshift")
        .option("url", "jdbc:redshift://src_redshift_host:port/src_database")
        .option("tempdir", "s3n://src_temp-bucket/temp-dir")
        .option("dbtable", table)
        .option("forward_spark_s3_credentials", "true")
        .load()
    )

    # Save dataframe to destination redshift
    data.write.format("com.databricks.spark.redshift").option(
        "url", "jdbc:redshift://dest_redshift_host:port/dest_database"
    ).option("tempdir", "s3n://dest_temp-bucket/temp-dir").option(
        "dbtable", table
    ).option(
        "forward_spark_s3_credentials", "true"
    ).option(
        "extracopyoptions", "TRUNCATECOLUMNS"
    ).mode(
        "overwrite"
    ).save()


# Create a pool of processes
pool = mp.Pool(processes=len(tables))

# Run the migration function for each table in parallel
pool.map(migrate_table, tables)

# Close the pool
pool.close()
pool.join()

"""
This code uses the multiprocessing library to run the migration of multiple tables in parallel. It creates a pool of processes, where the number of processes is equal to the number of tables. The migration of each table is done by the migrate_table function, which reads the data from the source Redshift database and writes it to the destination Redshift database. The pool.map() function applies the migrate_table function to each table in the tables list in parallel, using the processes in the pool. Finally, it closes the pool and waits for all the processes to finish.

You should change the redshift host, port, tempdir, database and table name accordingly with your own redshift configurations.
"""
