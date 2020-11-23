from copy import deepcopy
from typing import Iterable

from query_filter import predicates


def _simple_keywords_predicate(filter_kwargs: dict):

    def predicate(item):
        for key, value in filter_kwargs.items():

            if key not in item or item[key] != value:
                return False

        return True

    return predicate


def qfilter(items: Iterable, *predicates, **kwargs):
    items_copy = deepcopy(items)
    
    kwargs_predicate = _simple_keywords_predicate(kwargs)

    def main_predicate(item):
        if not kwargs_predicate(item):
            return False

        return all(predicate(item) for predicate in predicates)
    
    return filter(main_predicate, items_copy)


class Attr:
    def __init__(self, *names):
        self._names = names

    def __eq__(self, other):
        return predicates.Equals(self._names, other, use_attrs=True)


class Item:
    def __init__(self, *keys):
        self._keys = keys

    def __eq__(self, other):
        return predicates.Equals(self._keys, other, use_attrs=False)

