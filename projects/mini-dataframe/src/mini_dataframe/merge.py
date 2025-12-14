# my_dataframe/merge.py


class MergeMixin:
    def join(self, other, on, how="inner", lsuffix="", rsuffix="_right"):
        if not isinstance(other, self.__class__):
            raise TypeError("Can only join MiniDataFrame to MiniDataFrame")
        left_map, right_map = {}, {}
        left_idx, right_idx = self.column_to_index[on], other.column_to_index[on]
        for r in self.data:
            left_map.setdefault(r[left_idx], []).append(r)
        for r in other.data:
            right_map.setdefault(r[right_idx], []).append(r)
        keys = {
            "inner": left_map.keys() & right_map.keys(),
            "left": left_map.keys(),
            "right": right_map.keys(),
            "outer": left_map.keys() | right_map.keys(),
        }[how]
        overlap = set(self.columns) & set(other.columns) - {on}
        l_cols = [c + lsuffix if c in overlap else c for c in self.columns]
        r_cols = [c + rsuffix if c in overlap else c for c in other.columns]
        out = []
        for k in keys:
            l_rows, r_rows = left_map.get(k, [None]), right_map.get(k, [None])
            for l in l_rows:
                for r in r_rows:
                    row = {}
                    row.update(
                        {
                            l_cols[i]: l[i] if l else None
                            for i in range(len(self.columns))
                        }
                    )
                    row.update(
                        {
                            r_cols[i]: r[i] if r else None
                            for i in range(len(other.columns))
                        }
                    )
                    out.append(row)
        return self.__class__({col: [r[col] for r in out] for col in out[0]})

    @classmethod
    def concat(cls, frames, axis=0):
        if axis == 0:
            cols = frames[0].columns
            if any(f.columns != cols for f in frames):
                raise ValueError("Columns must match for row concat")
            return cls({col: sum([f[col] for f in frames], []) for col in cols})
        if axis == 1:
            n = frames[0].n_rows
            if any(f.n_rows != n for f in frames):
                raise ValueError("Row count must match for column concat")
            merged = {}
            for f in frames:
                for c in f.columns:
                    if c in merged:
                        raise ValueError(f"Duplicate column: {c}")
                    merged[c] = f[c]
            return cls(merged)
        raise ValueError("Axis must be 0 (rows) or 1 (columns)")
