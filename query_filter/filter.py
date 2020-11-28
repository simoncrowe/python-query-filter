from copy import deepcopy
from functools import reduce
from itertools import chain, starmap
from operator import getitem
from typing import Any, Callable, Hashable, Iterable, Mapping

from query_filter import predicate


def qfilter(items: Iterable, *preds) -> Iterable[Any]:
    def main_predicate(item):
        return all(pred(item) for pred in preds)

    return (deepcopy(i) for i in filter(main_predicate, items))


class Query:
    def __init__(self, *keys, getter: Callable):
        self._keys = keys
        self._getter = getter

    def __lt__(self, criteria):
        return predicate.lt(criteria, self._getter, self._keys)

    def __le__(self, criteria):
        return predicate.lte(criteria, self._getter, self._keys)

    def __eq__(self, criteria):
        return predicate.eq(criteria, self._getter, self._keys)

    def __ne__(self, criteria):
        return predicate.ne(criteria, self._getter, self._keys)

    def __gt__(self, criteria):
        return predicate.gt(criteria, self._getter, self._keys)

    def __ge__(self, criteria):
        return predicate.gte(criteria, self._getter, self._keys)

    def is_in(self, criteria):
        return predicate.is_in(criteria, self._getter, self._keys)

    def contains(self, criteria):
        return predicate.contains(criteria, self._getter, self._keys)

    def _is(self, criteria):
        return predicate._is(criteria, self._getter, self._keys)

    def _is_not(self, criteria):
        return predicate._is_not(criteria, self._getter, self._keys)


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


_filter_preds = {
    "lt": predicate.lt,
    "lte": predicate.lte,
    "eq": predicate.eq,
    "ne": predicate.ne,
    "gt": predicate.gt,
    "gte": predicate.gte,
    "in": predicate.is_in,
    "contains": predicate.contains,
    "is": predicate._is,
    "is_not": predicate._is_not,
}


def split_key(key: str):
    *keys, operation_name = key.split("__")

    # equality is used by defaul
    if operation_name not in _filter_preds:
        keys.append(operation_name)
        operation_name = "eq"

    if not keys or not all(bool(key) for key in keys):
        raise ValueError(
            "No part of the key-path may be an empty string. e.g. "
            "These are not allowed: '__bar_eq', 'foo__bar__', ''"
        )

    return keys, operation_name


def kpredicate(key: str, value: Any, getter: Callable):
    keys, operation_name = split_key(key)
    filter_pred = _filter_preds[operation_name]
    return filter_pred(value, getter, keys)


def kfilter(items: Iterable, getter: Callable, *preds, **kwargs):
    args = ((key, value, getter) for key, value in kwargs.items())
    kpreds = starmap(kpredicate, args)
    return qfilter(items, *chain(preds, kpreds))
