from copy import deepcopy
from functools import reduce
from operator import getitem
from typing import Any, Callable,Hashable, Iterable, Mapping

from query_filter import predicates


def _simple_keywords_predicate(filter_kwargs: dict):

    def predicate(item):
        for key, value in filter_kwargs.items():

            if key not in item or item[key] != value:
                return False

        return True

    return predicate


def qfilter(items: Iterable, *predicates, **kwargs) -> Iterable[Any]:
    kwargs_predicate = _simple_keywords_predicate(kwargs)

    def main_predicate(item):
        if not kwargs_predicate(item):
            return False

        return all(predicate(item) for predicate in predicates)
    
    return (deepcopy(i) for i in filter(main_predicate, items))


class Query:
    def __init__(self, *keys, getter: Callable):
        self._keys = keys
        self._getter

    def __lt__(self, other):
        return predicates.LessThan(self._keys, other, self._getter)

    def __le__(self, other):
        return predicates.LessThanOrEqual(self._keys, other, self._getter)

    def __eq__(self, other):
        return predicates.Equal(self._keys, other, self._getter)

    def __ne__(self, other):
        return predicates.NotEqual(self._keys, other, self._getter)

    def __gt__(self, other):
        return predicates.GreaterThan(self._keys, other, self._getter)

    def __ge__(self, other):
        return predicates.GreaterThanOrEqual(self._keys, other, self._getter)

    def is_in(self, other):
        return predicates.IsIn(self._keys, other, self._getter)

    def contains(self, other):
        return predicates.Contains(self._keys, other, self._getter)


def retrieve_attr(obj: Any, *names: str):
    try:
        return reduce(getattr, names, obj)
    except AttributeError:
        return None


class Attr(Query):
    def __init__(self, names: str, getter=retrieve_attr):
        self._keys = names.split(".")
        self._getter = getter


def retrieve_item(obj: Mapping, *keys: Hashable):
    try:
        return reduce(getitem, keys, obj)
    except (IndexError, KeyError, TypeError):
        return None


class Item(Query):
    def __init__(self, *keys: Iterable[Hashable], getter=retrieve_item):
        self._keys = keys
        self._getter = getter

