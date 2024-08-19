import redshift_connector
import logging
import time
import os

logging.basicConfig(level=logging.INFO)


def unload(conn, s3Bucket, iamRole, schema):
    start = time.time()
    cursor: redshift_connector.Cursor = conn.cursor()
    cursor.execute(
        "select table_name from information_schema.tables where "
        f"table_schema = '{schema}' and table_type = 'BASE TABLE' order by table_name;"
    )
    for table in cursor.fetchall():
        try:
            sql = (
                f"UNLOAD('select * from {schema}.{table[0]}') to "
                f"'{s3Bucket}/{table[0]}.gz' "
                f"iam_role '{iamRole}' "
                "ALLOWOVERWRITE parallel off CSV gzip;"
            )
            logging.info(f"Start unloading table:{table}")
            logging.info(sql)
            cursor.execute(sql)
            logging.info(f"End unloading table:{table}")
        except Exception as e:
            logging.error(f"Error in copying table:{table}. {e}")

    end = time.time()
    logging.info(f"Finished unloading all the table in {end - start} sec.")


def copy(conn, s3Bucket, iamRole, schema):
    start = time.time()
    cursor: redshift_connector.Cursor = conn.cursor()
    cursor.execute(
        "select table_name from information_schema.tables where "
        f"table_schema = '{schema}' and table_type = 'BASE TABLE' order by table_name;"
    )
    for table in cursor.fetchall():
        try:
            sql = (
                f"COPY {schema}.{table[0]} "
                f"from '{s3Bucket}/{table[0]}.gz' "
                f"iam_role '{iamRole}' "
                "CSV gzip;"
            )
            logging.info(f"Start copying table:{table}")
            logging.info(sql)
            cursor.execute(f"TRUNCATE {schema}.{table[0]}")
            cursor.execute(sql)
            conn.commit()
            logging.info(f"End copying table:{table}")
        except Exception as e:
            conn.rollback()
            logging.error(f"Error in copying table:{table}. {e}")

    end = time.time()
    logging.info(f"Finished copying all the table in {end - start} sec.")


if __name__ == "__main__":
    # Creating connection to database by reading database parameters from environment variable.
    connProd = redshift_connector.connect(
        host=os.environ["REDSHIFT_CLUSTER_ENDPOINT"],
        port=os.environ["REDSHIFT_DATABASE_PORT"],
        database=os.environ["REDSHIFT_DATABASE_NAME"],
        user=os.environ["REDSHIFT_DATABASE_USERNAME"],
        password=os.environ["REDSHIFT_DATABASE_PASSWORD"],
    )
    iamRoleProd = os.environ["IAM_ROLE_ARN"]
    s3Bucket = os.environ["S3_BUCKET_ARN"]
    schema = (os.environ["REDSHIFT_DATABASE_SCHEMA"],)

    # Calling unload function.
    unload(connProd, s3Bucket, iamRoleProd, schema)

    connTest = redshift_connector.connect(
        host=os.environ["REDSHIFT_CLUSTER_ENDPOINT"],
        port=os.environ["REDSHIFT_DATABASE_PORT"],
        database=os.environ["REDSHIFT_DATABASE_NAME"],
        user=os.environ["REDSHIFT_DATABASE_USERNAME"],
        password=os.environ["REDSHIFT_DATABASE_PASSWORD"],
    )

    iamRoleTest = os.environ["IAM_ROLE_ARN"]
    s3Bucket = os.environ["S3_BUCKET_ARN"]
    schema = (os.environ["REDSHIFT_DATABASE_SCHEMA"],)

    copy(connTest, s3Bucket, iamRoleTest, schema)
