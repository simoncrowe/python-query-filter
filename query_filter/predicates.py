from abc import ABC, abstractmethod
from functools import reduce
from operator import getitem
from typing import Any, Hashable, Iterable, Mapping


def retrieve_attr(obj: Any, names: Iterable[str]):
    try:
        return reduce(getattr, names, obj)
    except AttributeError:
        return None


def retrieve_item(obj: Mapping, keys: Iterable[Any]):
    try:
        return reduce(getitem, keys, obj)
    except KeyError:
        return None


class Predicate(ABC):

    def __init__(self, keys: Iterable[Hashable], criteria: Any):
        self._keys = keys
        self._criteria = criteria

    def __call__(self, obj: Any, attrs: bool) -> bool:
        if attrs:
            evaluated_obj = retrieve_attr(obj, self._keys)
        else:
            evaluated_obj = retrieve_item(obj, self._keys)

        if not evaluated_obj:
            return False

        return self.evaluate(evaluated_obj, self._criteria)

    @abstractmethod
    def evaluate(obj: Any, criteria: Any) -> bool:
        pass


class Equals(Predicate):

    def evaluate(self, obj: Any, criteria: Any):
        return obj == criteria

