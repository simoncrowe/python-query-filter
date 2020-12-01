from functools import reduce
from operator import getitem
from typing import Any, Callable, Hashable, Iterable, Iterator, Mapping

from query_filter import predicate


def q_filter_any(items: Iterable, *preds) -> Iterable[Any]:
    def main_predicate(item):
        return any(pred(item) for pred in preds)

    return filter(main_predicate, items)


def q_filter_not_any(items: Iterable, *preds) -> Iterable[Any]:
    def main_predicate(item):
        return not any(pred(item) for pred in preds)

    return filter(main_predicate, items)


def q_filter_all(items: Iterable, *preds, copy=True) -> Iterable[Any]:
    def main_predicate(item):
        return all(pred(item) for pred in preds)

    return filter(main_predicate, items)


q_filter = q_filter_all


def q_all(*preds: Callable) -> Callable:
    def all_pred(obj: Any):
        return all(pred(obj) for pred in preds)
    return all_pred


def q_any(*preds: Callable) -> Callable:
    def all_pred(obj: Any):
        return any(pred(obj) for pred in preds)
    return all_pred


def q_not(pred: Callable) -> Callable:
    def not_pred(obj: Any):
        return not pred(obj)
    return not_pred


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


def q_attr(path: str):
    return Query(*path.split(), getter=retrieve_attr)


def retrieve_item(obj: Mapping, *keys: Hashable):
    try:
        return reduce(getitem, keys, obj)
    except (IndexError, KeyError, TypeError):
        return None


def q_item(*keys: Hashable):
    return Query(*keys, getter=retrieve_item)


_pred_makers = {
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

    if operation_name not in _pred_makers:
        keys.append(operation_name)
        operation_name = "eq"

    if not keys or not all(bool(key) for key in keys):
        raise ValueError(
            "No part of the key-path may be an empty string. e.g. "
            "These are not allowed: '__bar_eq', 'foo__bar__', ''"
        )

    return keys, operation_name


def _kwarg_preds(kwargs: Mapping, getter: Callable) -> Iterator[Callable]:
    for key, value in kwargs.items():
        key_path, operation_name = split_key(key)
        filter_pred = _pred_makers[operation_name]
        yield filter_pred(value, getter, key_path)


def k_attrs_all(**kwargs) -> Callable:
    return q_all(*_kwarg_preds(kwargs, retrieve_attr))


def k_attrs_any(**kwargs) -> Callable:
    return q_any(*_kwarg_preds(kwargs, retrieve_attr))


def k_attrs_not_any(**kwargs) -> Callable:
    return q_not(q_any(*_kwarg_preds(kwargs, retrieve_attr)))


def k_items_all(**kwargs) -> Callable:
    return q_all(*_kwarg_preds(kwargs, retrieve_item))


def k_items_any(**kwargs) -> Callable:
    return q_any(*_kwarg_preds(kwargs, retrieve_item))


def k_items_not_any(getter: Callable, **kwargs) -> Callable:
    return q_not(q_any(*_kwarg_preds(kwargs, retrieve_item)))


k_attrs = k_attrs_all
k_items = k_items_all
