from abc import ABC, abstractmethod
from typing import Any, Callable
import os
import pickle
from dataclasses import dataclass, field
import requests


class CacheInterface(ABC):
    """Interface for caching"""

    def __enter__(self):
        raise NotImplementedError
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        raise NotImplementedError

    @abstractmethod
    def put(self, key: str, data: Any) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(self, key: str) -> Any:
        raise NotImplementedError


@dataclass
class LocalCache(CacheInterface):
    """Implementation of cache interface to provide a local cache
    in the form of key pair value saved in a pickle file"""

    path: str
    cache: dict = field(init=False)

    def __post_init__(self):
        self.cache = {}
        if os.path.isfile(self.path):
            self.load_cache()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.dump_cache()

    def load_cache(self):
        with open(self.path, "rb") as cache:
            self.cache = pickle.load(cache)

    def dump_cache(self):
        with open(self.path, "wb") as cache:
            self.cache = pickle.dump(self.cache, cache)

    def put(self, key: str, data: Any) -> None:
        self.cache[key] = data

    def get(self, key: str) -> Any:
        return self.cache[key]


urls = [f"https://jsonplaceholder.typicode.com/comments/{id_}" for id_ in range(1, 5)]

with LocalCache("cache.pickle") as cache:
    for url in urls:
        try:
            data = cache.get(url)
            print(f"hit cache: {data}")
        except KeyError as err:
            resp = requests.get(url)
            cache.put(url, resp.json())
