import collections
from typing import Any, Callable, Type, TypeVar

from collections.abc import MutableMapping


def flatten(dictionary, parent_key=False, separator="."):
    items = []
    for key, value in dictionary.items():
        new_key = str(parent_key) + separator + key if parent_key else key
        if isinstance(value, collections.MutableMapping):
            items.extend(flatten(value, new_key, separator).items())
        elif isinstance(value, list):
            for k, v in enumerate(value):
                items.extend(flatten({str(k): v}, new_key).items())
        else:
            items.append((new_key, value))
    return dict(items)


def flatten_dict(dictionary, accumulator=None, parent_key=None, separator="."):
    if accumulator is None:
        accumulator = {}
    for k, v in dictionary.items():
        k = f"{parent_key}{separator}{k}" if parent_key else k
        if isinstance(v, dict):
            flatten_dict(dictionary=v, accumulator=accumulator, parent_key=k)
            continue
        accumulator[k] = v

    return accumulator


def _flatten_dict_gen(d, parent_key, sep):
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, MutableMapping):
            yield from flatten_dict_generator(v, new_key, sep=sep).items()
        else:
            yield new_key, v


def flatten_dict_generator(d: MutableMapping, parent_key: str = "", sep: str = "."):
    return dict(_flatten_dict_gen(d, parent_key, sep))


def flatten_(d, sep="_"):
    obj = collections.OrderedDict()

    def recurse(t, parent_key=""):
        if isinstance(t, list):
            for i in range(len(t)):
                recurse(t[i], parent_key + sep + str(i) if parent_key else str(i))
        elif isinstance(t, dict):
            for k, v in t.items():
                recurse(v, parent_key + sep + k if parent_key else k)
        else:
            obj[parent_key] = t

    recurse(d)
    return obj
