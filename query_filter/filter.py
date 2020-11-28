from copy import deepcopy
from functools import reduce
from operator import getitem
from typing import Any, Hashable, Iterable, Mapping

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


def retrieve_attr(obj: Any, names: Iterable[str]):
    try:
        return reduce(getattr, names, obj)
    except AttributeError:
        return None


class Attr:
    def __init__(self, *names):
        self._names = names

    def __eq__(self, other):
        return predicates.Equals(self._names, other, getter=retrieve_attr)


def retrieve_item(obj: Mapping, keys: Iterable[Hashable]):
    try:
        return reduce(getitem, keys, obj)
    except KeyError:
        return None


class Item:
    def __init__(self, *keys):
        self._keys = keys

    def __eq__(self, other):
        return predicates.Equals(self._keys, other, getter=retrieve_item)

