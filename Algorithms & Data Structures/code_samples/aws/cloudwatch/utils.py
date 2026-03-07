from abc import ABC, abstractmethod
from typing import Any, Callable
import boto3
import functools
import logging
from botocore.exceptions import ClientError

try:
    from .config import boto3_config
except ImportError as e:
    boto3_config = {}

logger = logging.getLogger(__name__)


class AbstractDecorator(ABC):
    def __init__(self, decorated: Callable[..., Any]) -> None:
        self._decorated = decorated

    @abstractmethod
    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError


class Unwrap(AbstractDecorator):
    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        results = []
        continuation_token = None
        try:
            while True:
                list_kwargs = {}
                list_kwargs.update(**kwargs)
                if continuation_token:
                    list_kwargs["Marker"] = continuation_token
                response = self._decorated(*args, **list_kwargs)
                results += response.get(f"{'Functions'}", [])
                continuation_token = response.get("NextMarker")
                if not continuation_token:
                    break
        except ClientError as err:
            logger.error(
                f"Couldn't list functions. Here's why: {err.response['Error']['Code']}: {err.response['Error']['Message']}",
            )
            raise
        else:
            return results


class LamdaFunctions:
    @functools.cached_property
    def lambda_client(self):
        return boto3.client("lambda", **boto3_config)

    @functools.lru_cache
    @Unwrap
    def functions(self, *args, **kwargs):
        list_kwargs = {}
        list_kwargs.update(**kwargs)
        return self.lambda_client.list_functions(**list_kwargs)
