from psycopg2.extras import DictCursor
from psycopg2.pool import SimpleConnectionPool


class Database:
    __pool = None

    @classmethod
    def initialize(cls, **kwargs):
        cls.__pool = SimpleConnectionPool(
            minconn=2, maxconn=5, cursor_factory=DictCursor, **kwargs
        )

    @classmethod
    def get_connection(cls):
        return cls.__pool.getconn()

    @classmethod
    def return_connection(cls, connection):
        Database.__pool.putconn(connection)

    @classmethod
    def close_all_connections(cls):
        Database.__pool.closeall()


class CursorFromConnectionFromPool:
    """Get a cursor from a connection from pool of connections."""

    def __init__(self):
        self.connection = None
        self.cursor = None

    def __enter__(self):
        # get a connection from the pool
        self.connection = Database.get_connection()

        # get a cursor, the is to reduce one more step after getting
        # the connection, becuase we always want a cursor
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Rollback if not everything is good
        if exc_val is not None:
            self.connection.rollback()
        else:
            self.cursor.close()

            # commit the connection otherwise nothing is gonna write
            self.connection.commit()

        # put it back to pool
        Database.return_connection(self.connection)
