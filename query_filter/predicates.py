from abc import ABC, abstractmethod
from functools import reduce
from operator import getitem
from typing import Any, Callable, Hashable, Iterable, Mapping


def retrieve_item(obj: Mapping, keys: Iterable[Hashable]):
    try:
        return reduce(getitem, keys, obj)
    except KeyError:
        return None


class Predicate(ABC):

    def __init__(self,
                 keys: Iterable[Hashable],
                 criteria: Any,
                 getter: Callable):

        self._keys = keys
        self._criteria = criteria
        self._get = getter

    def __call__(self, obj: Any) -> bool:
        evaluated_obj = self._get(obj, self._keys)

        if evaluated_obj is None:
            return False

        return self.evaluate(evaluated_obj, self._criteria)

    @abstractmethod
    def evaluate(obj: Any, criteria: Any) -> bool:
        pass


class Equals(Predicate):

    def evaluate(self, obj: Any, criteria: Any):
        return obj == criteria

