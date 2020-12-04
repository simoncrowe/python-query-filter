from functools import reduce
from operator import getitem
import re
from typing import Any, Callable, Hashable, Iterable, Iterator, Mapping

from query_filter.filter import q_all, q_any, q_not


class Query:
    def __init__(self, *keys, getter: Callable):
        self._keys = keys
        self._getter = getter

    def __lt__(self, criteria):
        return lt(self._getter, self._keys, criteria)

    def __le__(self, criteria):
        return lte(self._getter, self._keys, criteria)

    def __eq__(self, criteria):
        return eq(self._getter, self._keys, criteria)

    def __ne__(self, criteria):
        return ne(self._getter, self._keys, criteria)

    def __gt__(self, criteria):
        return gt(self._getter, self._keys, criteria)

    def __ge__(self, criteria):
        return gte(self._getter, self._keys, criteria)

    def is_in(self, container):
        return is_in(self._getter, self._keys, container)

    def contains(self, member):
        return contains(self._getter, self._keys, member)

    def regex(self, pattern):
        return regex(self._getter, self._keys, pattern)

    def is_none(self):
        return is_none(self._getter, self._keys)

    def is_not_none(self):
        return is_not_none(self._getter, self._keys)

    def is_true(self):
        return is_true(self._getter, self._keys)

    def is_false(self):
        return is_false(self._getter, self._keys)


class ObjNotFound(Exception):
    """Raised when the requested attr or item is not found."""


def retrieve_attr(obj: Any, *names: str):
    try:
        return reduce(getattr, names, obj)
    except AttributeError:
        raise ObjNotFound()


def q_attr(path: str):
    return Query(*path.split(), getter=retrieve_attr)


def retrieve_item(obj: Mapping, *keys: Hashable):
    try:
        return reduce(getitem, keys, obj)
    except (IndexError, KeyError, TypeError):
        raise ObjNotFound()


def q_item(*keys: Hashable):
    return Query(*keys, getter=retrieve_item)


def query_predicate(predicate: Callable):
    """
    Decorates predicate functions.

    The immediate output is a function that accepts an object is to be
    evaluated and the means of getting this object from a "root" object.
    This funtion returns a predicate that evaluates any "root" object
    using the decorated function.
    """
    def pred_maker(get: Callable, keys: Iterable[Any]):

        def pred(obj: Any):
            try:
                evaluated = get(obj, *keys)
            except ObjNotFound:
                return False
            return predicate(evaluated)

        return pred

    return pred_maker


def query_criteria(comparer: Callable):
    """
    Like query_predicate, but decorates functions that evaluate an object
    against some criteria.
    """
    def pred_maker(get: Callable, keys: Iterable[Any], *criteria: Any):

        def pred(obj: Any):
            try:
                evaluated = get(obj, *keys)
            except ObjNotFound:
                return False

            return comparer(evaluated, *criteria)

        return pred

    return pred_maker


@query_criteria
def lt(evaluated: Any, criteria: Any):
    return evaluated < criteria


@query_criteria
def lte(obj: Any, criteria: Any):
    return obj <= criteria


@query_criteria
def eq(obj: Any, criteria: Any):
    return obj == criteria


@query_criteria
def ne(obj: Any, criteria: Any):
    return obj != criteria


@query_criteria
def gt(obj: Any, criteria: Any):
    return obj > criteria


@query_criteria
def gte(obj: Any, criteria: Any):
    return obj >= criteria


@query_criteria
def is_in(obj: Any, criteria: Any):
    return obj in criteria


@query_criteria
def contains(obj: Any, criteria: Any):
    return criteria in obj


@query_criteria
def _is(obj: Any, criteria: Any):
    return obj is criteria


@query_criteria
def _is_not(obj: Any, criteria: Any):
    return obj is not criteria


@query_criteria
def regex(obj: str or bytes, pattern: str or bytes):
    return bool(re.search(pattern, obj))


@query_predicate
def is_none(obj: Any):
    return obj is None


@query_predicate
def is_not_none(obj: Any):
    return obj is not None


@query_predicate
def is_true(obj: Any):
    return obj is True


@query_predicate
def is_false(obj: Any):
    return obj is False


_query_map = {
    "lt": lt,
    "lte": lte,
    "eq": eq,
    "ne": ne,
    "gt": gt,
    "gte": gte,
    "in": is_in,
    "contains": contains,
    "regex": regex,
    "is": _is,
    "is_not": _is_not,
}


def split_key(key: str):
    *keys, operation_name = key.split("__")

    if operation_name not in _query_map:
        keys.append(operation_name)
        operation_name = "eq"

    if not keys or not all(bool(key) for key in keys):
        raise ValueError(
            "No part of the key-path may be an empty string. e.g. "
            "These are not allowed: '__bar__eq', 'foo__bar__', ''"
        )

    return keys, operation_name


def split_attr_key(key: str):
    if "__" in key:
        key, operation_name = key.split("__")
    else:
        operation_name = "eq"

    if operation_name not in _query_map:
        raise ValueError(
            f"'{operation_name}' is not a valid opration. "
            f"Options are {', '.join(_query_map.keys())}"
        )

    keys = key.split(".")

    if not keys or not all(bool(key) for key in keys):
        raise ValueError(
            "No part of the key-path may be an empty string. e.g. "
            "These are not allowed: '.bar__eq', 'foo.bar.', ''"
        )

    return keys, operation_name


def _kwarg_preds_items(kwargs: Mapping) -> Iterator[Callable]:
    for key, value in kwargs.items():
        key_path, operation_name = split_key(key)
        filter_pred = _query_map[operation_name]
        yield filter_pred(retrieve_item, key_path, value)


def _kwarg_preds_attrs(kwargs: Mapping) -> Iterator[Callable]:
    for key, value in kwargs.items():
        key_path, operation_name = split_attr_key(key)
        filter_pred = _query_map[operation_name]
        yield filter_pred(retrieve_attr, key_path, value)


def k_attrs_all(**kwargs) -> Callable:
    return q_all(*_kwarg_preds_attrs(kwargs))


def k_attrs_any(**kwargs) -> Callable:
    return q_any(*_kwarg_preds_attrs(kwargs))


def k_attrs_not_any(**kwargs) -> Callable:
    return q_not(q_any(*_kwarg_preds_attrs(kwargs)))


def k_items_all(**kwargs) -> Callable:
    return q_all(*_kwarg_preds_items(kwargs))


def k_items_any(**kwargs) -> Callable:
    return q_any(*_kwarg_preds_items(kwargs))


def k_items_not_any(**kwargs) -> Callable:
    return q_not(q_any(*_kwarg_preds_items(kwargs)))


k_attrs = k_attrs_all
k_items = k_items_all
