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
        self._getter = getter

    def __lt__(self, other):
        return predicates.lt(other, self._getter, self._keys)

    def __le__(self, other):
        return predicates.lte(other, self._getter, self._keys)

    def __eq__(self, other):
        return predicates.eq(other, self._getter, self._keys)

    def __ne__(self, other):
        return predicates.ne(other, self._getter, self._keys)

    def __gt__(self, other):
        return predicates.gt(other, self._getter, self._keys)

    def __ge__(self, other):
        return predicates.gte(other, self._getter, self._keys)

    def is_in(self, other):
        return predicates.is_in(other, self._getter, self._keys)

    def contains(self, other):
        return predicates.contains(other, self._getter, self._keys)

    def _is(self, other):
        return predicates._is(other, self._getter, self._keys)

    def _is_not(self, other):
        return predicates._is_not(other, self._getter, self._keys)


def retrieve_attr(obj: Any, *names: str):
    try:
        return reduce(getattr, names, obj)
    except AttributeError:
        return None


def attr(path: str):
    return Query(*path.split(), getter=retrieve_attr)


def retrieve_item(obj: Mapping, *keys: Hashable):
    try:
        return reduce(getitem, keys, obj)
    except (IndexError, KeyError, TypeError):
        return None


def item(*keys: Hashable):
    return Query(*keys, getter=retrieve_item)

