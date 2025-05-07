

class DatabasePrototype:
    """Database Prototype class"""

    _instance = None

    def __init__(self):
        raise RuntimeError('Call instance() instead')

    @classmethod
    def instance(cls):
        if cls._instance is None:
            print('Creating new instance')
            cls._instance = cls.__new__(cls)
        return cls._instance

    @staticmethod
    def query(query: str) -> str:
        print(f'Running SQL query: {query}')
        return f'Result for {query}'
