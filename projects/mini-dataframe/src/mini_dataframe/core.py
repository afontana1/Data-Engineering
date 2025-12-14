# my_dataframe/core.py

import math
import csv
import json
from collections import Counter, defaultdict
from .base import AbstractFrame, AbstractStatMixin, AbstractTransformationsMixin
from .dsl import QueryDSL


class BaseFrame(AbstractFrame):
    def __init__(self, data):
        if not data:
            raise ValueError("Data cannot be empty")
        self.columns = list(data.keys())
        self.column_to_index = {col: i for i, col in enumerate(self.columns)}
        self.n_cols = len(self.columns)
        lengths = {len(col_data) for col_data in data.values()}
        if len(lengths) != 1:
            raise ValueError("All columns must have same length")
        self.data = list(zip(*[data[col] for col in self.columns]))
        self.n_rows = len(self.data)

    def shape(self):
        return (self.n_rows, self.n_cols)

    def head(self, n=5):
        return self._preview(self.data[:n])

    def tail(self, n=5):
        return self._preview(self.data[-n:])

    def _preview(self, rows):
        return [self.columns] + [
            [row[self.column_to_index[col]] for col in self.columns] for row in rows
        ]

    def __repr__(self):
        return "\n".join([" | ".join(map(str, row)) for row in self.head(5)])

    def iloc(self, index):
        return (
            {col: self.data[index][i] for i, col in enumerate(self.columns)}
            if isinstance(index, int)
            else self.__class__(
                {
                    col: [row[i] for row in self.data[index]]
                    for i, col in enumerate(self.columns)
                }
            )
        )

    def loc(self, cond):
        rows = [
            row
            for row in self.data
            if cond({col: row[i] for i, col in enumerate(self.columns)})
        ]
        return self.__class__(
            {col: [row[i] for row in rows] for i, col in enumerate(self.columns)}
        )

    def __getitem__(self, col):
        return (
            [row[self.column_to_index[col]] for row in self.data]
            if isinstance(col, str)
            else self.__class__({c: self[c] for c in col})
        )

    def add_column(self, name, values):
        self.columns.append(name)
        self.column_to_index[name] = len(self.columns) - 1
        self.data = [row + (val,) for row, val in zip(self.data, values)]
        self.n_cols += 1

    def drop(self, cols):
        return self.__class__(
            {
                col: self[col]
                for col in self.columns
                if col not in (cols if isinstance(cols, list) else [cols])
            }
        )

    def rename(self, renamer):
        self.columns = [renamer.get(c, c) for c in self.columns]
        self.column_to_index = {c: i for i, c in enumerate(self.columns)}

    def sort_by(self, col, reverse=False):
        self.data.sort(key=lambda row: row[self.column_to_index[col]], reverse=reverse)

    def apply(self, func, col):
        idx = self.column_to_index[col]
        return [func(row[idx]) for row in self.data]


class StatMixin(AbstractStatMixin):
    def _numeric(self, col):
        return [v for v in self[col] if isinstance(v, (int, float))]

    def mean(self, col):
        return sum(self._numeric(col)) / len(self._numeric(col))

    def sum(self, col):
        return sum(self._numeric(col))

    def min(self, col):
        return min(self._numeric(col))

    def max(self, col):
        return max(self._numeric(col))

    def count(self, col):
        return len([v for v in self[col] if v is not None])

    def median(self, col):
        vals = sorted(self._numeric(col))
        n = len(vals)
        return vals[n // 2] if n % 2 else (vals[n // 2 - 1] + vals[n // 2]) / 2

    def variance(self, col):
        vals = self._numeric(col)
        m = self.mean(col)
        return sum((x - m) ** 2 for x in vals) / (len(vals) - 1)

    def std(self, col):
        return math.sqrt(self.variance(col))

    def mode(self, col):
        freq = Counter([v for v in self[col] if v is not None])
        max_freq = max(freq.values(), default=0)
        return [k for k, v in freq.items() if v == max_freq]

    def quantile(self, col, q):
        vals = sorted(self._numeric(col))
        idx = int(q * (len(vals) - 1))
        return vals[idx]

    def describe(self):
        desc = {}
        for col in self.columns:
            values = [v for v in self[col] if v is not None]
            if not values:
                desc[col] = {}
                continue
            sample = values[0]
            if isinstance(sample, (int, float)):
                desc[col] = {
                    "count": self.count(col),
                    "mean": self.mean(col),
                    "std": self.std(col),
                    "min": self.min(col),
                    "25%": self.quantile(col, 0.25),
                    "50%": self.median(col),
                    "75%": self.quantile(col, 0.75),
                    "max": self.max(col),
                    "mode": self.mode(col),
                }
            else:
                freq = Counter(values)
                top, top_freq = freq.most_common(1)[0]
                desc[col] = {
                    "count": len(values),
                    "unique": len(set(values)),
                    "top": top,
                    "freq": top_freq,
                    "mode": self.mode(col),
                }
        return desc


class TransformationsMixin(AbstractTransformationsMixin):
    def group_by(self, by_col):
        idx = self.column_to_index[by_col]
        groups = defaultdict(list)
        [groups[row[idx]].append(row) for row in self.data]
        return {
            k: self.__class__(
                {
                    col: [r[self.column_to_index[col]] for r in rows]
                    for col in self.columns
                }
            )
            for k, rows in groups.items()
        }

    def filter_rows(self, pred):
        return self.__class__(
            {
                col: [
                    row[i]
                    for row in self.data
                    if pred({c: row[j] for j, c in enumerate(self.columns)})
                ]
                for i, col in enumerate(self.columns)
            }
        )

    def map_column(self, col, func):
        idx = self.column_to_index[col]
        new = [
            tuple(func(v) if i == idx else v for i, v in enumerate(row))
            for row in self.data
        ]
        return self.__class__(
            {col: [row[i] for row in new] for i, col in enumerate(self.columns)}
        )

    def drop_duplicates(self, subset=None):
        subset = subset or self.columns
        seen, out = set(), []
        idxs = [self.column_to_index[c] for c in subset]
        [
            (
                out.append(r)
                if (key := tuple(r[i] for i in idxs)) not in seen and not seen.add(key)
                else None
            )
            for r in self.data
        ]
        return self.__class__(
            {
                col: [row[self.column_to_index[col]] for row in out]
                for col in self.columns
            }
        )

    def query(self, expr):
        return self.filter_rows(QueryDSL.build_filter(expr))

    def select(self, *cols, where=None):
        df = self.query(where) if where else self
        return df if cols == ("*",) else df[[c for c in cols]]


class IOOperationsMixin:
    @classmethod
    def from_csv(cls, path, delimiter=","):
        with open(path) as f:
            r = csv.DictReader(f, delimiter=delimiter)
            d = {}
            [
                d.setdefault(k, []).append(cls._convert(v))
                for row in r
                for k, v in row.items()
            ]
            return cls(d)

    @classmethod
    def from_json(cls, path):
        with open(path) as f:
            j = json.load(f)
            return (
                cls({k: [row.get(k) for row in j] for k in j[0]})
                if isinstance(j, list)
                else cls(j)
            )

    def to_csv(self, path, delimiter=","):
        with open(path, "w") as f:
            w = csv.DictWriter(f, fieldnames=self.columns, delimiter=delimiter)
            w.writeheader()
            [
                w.writerow(
                    {col: row[self.column_to_index[col]] for col in self.columns}
                )
                for row in self.data
            ]

    def to_json(self, path, indent=2):
        with open(path, "w") as f:
            json.dump(
                [
                    {col: row[self.column_to_index[col]] for col in self.columns}
                    for row in self.data
                ],
                f,
                indent=indent,
            )

    @staticmethod
    def _convert(val):
        return (
            int(val)
            if val.isdigit()
            else float(val) if val.replace(".", "", 1).isdigit() else val
        )
