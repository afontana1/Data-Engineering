# my_dataframe/base.py

from abc import ABC, abstractmethod


class AbstractFrame(ABC):
    @abstractmethod
    def shape(self):
        pass

    @abstractmethod
    def __getitem__(self, col):
        pass

    @abstractmethod
    def iloc(self, index):
        pass

    @abstractmethod
    def loc(self, condition):
        pass

    @abstractmethod
    def head(self, n=5):
        pass

    @abstractmethod
    def tail(self, n=5):
        pass

    @abstractmethod
    def add_column(self, name, values):
        pass

    @abstractmethod
    def drop(self, cols):
        pass

    @abstractmethod
    def rename(self, renamer: dict):
        pass

    @abstractmethod
    def sort_by(self, col, reverse=False):
        pass

    @abstractmethod
    def apply(self, func, col):
        pass


class AbstractStatMixin(ABC):
    @abstractmethod
    def mean(self, col):
        pass

    @abstractmethod
    def sum(self, col):
        pass

    @abstractmethod
    def min(self, col):
        pass

    @abstractmethod
    def max(self, col):
        pass

    @abstractmethod
    def count(self, col):
        pass

    @abstractmethod
    def median(self, col):
        pass

    @abstractmethod
    def variance(self, col):
        pass

    @abstractmethod
    def std(self, col):
        pass

    @abstractmethod
    def mode(self, col):
        pass

    @abstractmethod
    def quantile(self, col, q):
        pass

    @abstractmethod
    def describe(self):
        pass


class AbstractTransformationsMixin(ABC):
    @abstractmethod
    def group_by(self, by_col):
        pass

    @abstractmethod
    def filter_rows(self, predicate):
        pass

    @abstractmethod
    def map_column(self, col, func):
        pass

    @abstractmethod
    def drop_duplicates(self, subset=None):
        pass

    @abstractmethod
    def query(self, expr):
        pass

    @abstractmethod
    def select(self, *columns, where=None):
        pass
