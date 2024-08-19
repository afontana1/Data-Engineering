import os

def get_config():
    '''Setup parameters for postgres. Returns a data base url string.'''
    # Parameters for the RDS PostgreSQL instance
    PG_HOST = os.environ.get('PG_HOST')
    PG_PORT = os.environ.get('PG_PORT')
    PG_DATABASE = os.environ.get('PG_DATABASE')
    PG_USER = os.environ.get('PG_USER')
    PG_PASSWORD = os.environ.get('PG_PASSWORD')

    # Create the MySQL database connection string
    db_url = f'postgresql+psycopg2://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DATABASE}'
    
    return db_url