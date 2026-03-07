from weakref import WeakValueDictionary


class Flyweight:
    """Flyweight class"""

    # Could be a simple dict.
    # With WeakValueDictionary garbage collection can reclaim the object
    # when there are no other references to it.
    _pool: WeakValueDictionary = WeakValueDictionary()

    def __new__(cls, id: int | str = 0, val: str = '<default>'):
        obj = cls._pool.get(str(id) + val)
        if obj is None:
            obj = object.__new__(Flyweight)
            cls._pool[str(id) + val] = obj
            obj.id, obj.val = str(id), val  # type: ignore
        return obj

    def clear(self) -> None:
        self._pool.clear()

    def __repr__(self):
        return f'Flyweight #{self.id} ({self.val})'
