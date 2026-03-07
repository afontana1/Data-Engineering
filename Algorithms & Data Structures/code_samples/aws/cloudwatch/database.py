import psycopg2


class Database:
    def __init__(self, host, user, password, database, port):
        self.host = host
        self.user = user
        self.password = password
        self.dbname = database
        self.port = port

    def __enter__(self):
        try:
            conn = psycopg2.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                dbname=self.dbname,
                port=self.port,
            )
        except Exception as e:
            raise e
        setattr(self, "_conn", conn)
        setattr(self, "_cursor", self._conn.cursor())
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self._conn.rollback()
        self.close()

    @property
    def connection(self):
        return self._conn

    @property
    def cursor(self):
        return self._cursor

    def commit(self):
        self._conn.commit()
        return True

    def close(self, commit=True):
        if commit:
            self.commit()
        self._conn.close()
        return True

    def execute(self, sql, params=None):
        self._cursor.execute(sql, params or ())
        return True
