# my_dataframe/__init__.py

from .core import BaseFrame, StatMixin, TransformationsMixin, IOOperationsMixin
from .merge import MergeMixin


class MiniDataFrame(
    BaseFrame, StatMixin, TransformationsMixin, IOOperationsMixin, MergeMixin
):
    pass
