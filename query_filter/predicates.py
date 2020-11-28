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
                 keys: Any,
                 criteria: Any,
                 getter: Callable):

        self._keys = keys
        self._criteria = criteria
        self._get = getter

    def __call__(self, obj: Any) -> bool:
        evaluated_obj = self._get(obj, *self._keys)

        if evaluated_obj is None:
            return False

        return self.evaluate(evaluated_obj, self._criteria)

    @abstractmethod
    def evaluate(obj: Any, criteria: Any) -> bool:
        pass


class LessThan(Predicate):

    def evaluate(self, obj: Any, criteria: Any):
        return obj < criteria


class LessThanOrEqual(Predicate):

    def evaluate(selt, obj: Any, criteria: Any):
        return obj <= criteria


class Equal(Predicate):

    def evaluate(self, obj: Any, criteria: Any):
        return obj == criteria


class NotEqual(Predicate):

    def evaluate(selt, obj: Any, criteria: Any):
        return obj != criteria


class GreaterThan(Predicate):

    def evaluate(self, obj: Any, criteria: Any):
        return obj > criteria


class GreaterThanOrEqual(Predicate):

    def evaluate(selt, obj: Any, criteria: Any):
        return obj >= criteria


class IsIn(Predicate):

    def evaluate(selt, obj: Any, criteria: Any):
        return obj in criteria


class Contains(Predicate):

    def evaluate(selt, obj: Any, criteria: Any):
        return criteria in obj


class Is(Predicate):

    def evaluate(selt, obj: Any, criteria: Any):
        return obj is criteria


class IsNot(Predicate):

    def evaluate(selt, obj: Any, criteria: Any):
        return obj is not criteria

