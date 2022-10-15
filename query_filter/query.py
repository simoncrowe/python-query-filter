import dataclasses
import enum
import re
from functools import reduce
from operator import getitem
from typing import Any, Callable, Hashable, Iterable, Iterator, Mapping

from query_filter.filter import q_all, q_any, q_not


class LookupType(enum.Enum):
    ITEM = 1
    ATTR = 2


@dataclasses.dataclass(frozen=True)
class Lookup:
    lookup_type: LookupType
    key: Hashable


QUERY_METHOD_NAMES = ("is_in", "contains", "matches_regex", "is_none", "is_not_none")


class Query:
    def __init__(self, lookups=()):
        self._lookups = lookups

    def __getattribute__(self, name):
        if name == "_lookups":
            return super().__getattribute__(name)

        new_lookup = Lookup(lookup_type=LookupType.ATTR, key=name)
        return Query(self._lookups + (new_lookup,))

    def __getitem__(self, key):
        new_lookup = Lookup(lookup_type=LookupType.ITEM, key=key)
        return Query(self._lookups + (new_lookup,))

    def __call__(self, *args, **kwargs):
        """Allow a Query object to act as one of its methods if called."""
        if self._lookups:
            rightmost_lookup = self._lookups[-1]
            if rightmost_lookup.key in QUERY_METHOD_NAMES:
                # Mutate lookups to remove method name
                self._lookups = self._lookups[:-1]
                method = super().__getattribute__(rightmost_lookup.key)
                return method(*args, **kwargs)
            raise NotImplementedError(
                f"Cannot call Query for attribute name '{rightmost_lookup.key}'. "
                "Maybe you misspelled a method name."
            )
        raise NotImplementedError("Cannot call Query. Maybe you misspelled a method name")

    def __lt__(self, criterion: Any) -> Callable:
        return lt(self._lookups, criterion)

    def __le__(self, criterion: Any) -> Callable:
        return lte(self._lookups, criterion)

    def __eq__(self, criterion: Any) -> Callable:
        return eq(self._lookups, criterion)

    def __ne__(self, criterion: Any) -> Callable:
        return ne(self._lookups, criterion)

    def __gt__(self, criterion: Any) -> Callable:
        return gt(self._lookups, criterion)

    def __ge__(self, criterion: Any) -> Callable:
        return gte(self._lookups, criterion)

    def is_in(self, container: Any) -> Callable:
        return is_in(self._lookups, container)

    def contains(self, member: Any) -> Callable:
        return contains(self._lookups, member)

    def matches_regex(self, pattern: str) -> Callable:
        return regex(self._lookups, pattern)

    def is_none(self) -> Callable:
        return is_none(self._lookups)

    def is_not_none(self) -> Callable:
        return is_not_none(self._lookups)


class ObjNotFound(Exception):
    """Raised when the requested attr or item is not found."""


def retrieve_attr(obj: Any, *names: str):
    try:
        return reduce(getattr, names, obj)
    except AttributeError:
        raise ObjNotFound()


def q_attr(path: str) -> Query:
    return Query(*path.split("."), getter=retrieve_attr)


def retrieve_item(obj: Mapping, *keys: Hashable):
    try:
        return reduce(getitem, keys, obj)
    except (IndexError, KeyError, TypeError):
        raise ObjNotFound()


def q_item(*keys: Hashable) -> Query:
    return Query(*keys, getter=retrieve_item)


def retrieve_value(obj: Any, *lookups: Lookup):
    value = obj

    try:
        for lookup in lookups:
            if lookup.lookup_type == LookupType.ATTR:
                value = getattr(value, lookup.key)
            elif lookup.lookup_type == LookupType.ITEM:
                value = getitem(value, lookup.key)
            else:
                raise ValueError(f"{lookup.lookup_type} is not a valid lookup type")
    except (IndexError, KeyError, TypeError, AttributeError):
        raise ObjNotFound()

    return value


def query_predicate(predicate: Callable):
    """
    Decorates predicate functions, allowing them to be applied
    to nested "child" attributes or items of objects.

    The immediate output is a function that accepts a sequence of
    key or attribute names and a function that uses this sequence
    to get the desired "child" object from a "root" object.
    This function, in turn, returns a predicate that evaluates any "root"
    object using the decorated function.
    """
    def pred_maker(lookups: Iterable[Lookup]):

        def pred(obj: Any):
            try:
                evaluated = retrieve_value(obj, *lookups)
            except ObjNotFound:
                return False
            return predicate(evaluated)

        return pred

    return pred_maker


def query_criterion(comparer: Callable):
    """
    Like query_predicate, but decorates functions that evaluate
    a "child" object against some criterion.
    """
    def pred_maker(lookups: Iterable[Lookup], *criteria: Any):

        def pred(obj: Any):
            try:
                evaluated = retrieve_value(obj, *lookups)
            except ObjNotFound:
                return False

            return comparer(evaluated, *criteria)

        return pred

    return pred_maker


@query_criterion
def lt(evaluated: Any, criterion: Any):
    return evaluated < criterion


@query_criterion
def lte(obj: Any, criterion: Any):
    return obj <= criterion


@query_criterion
def eq(obj: Any, criterion: Any):
    return obj == criterion


@query_criterion
def ne(obj: Any, criterion: Any):
    return obj != criterion


@query_criterion
def gt(obj: Any, criterion: Any):
    return obj > criterion


@query_criterion
def gte(obj: Any, criterion: Any):
    return obj >= criterion


@query_criterion
def is_in(obj: Any, container: Any):
    return obj in container


@query_criterion
def contains(obj: Any, member: Any):
    return member in obj


@query_criterion
def _is(obj: Any, criterion: Any):
    return obj is criterion


@query_criterion
def _is_not(obj: Any, criterion: Any):
    return obj is not criterion


@query_criterion
def regex(obj: str or bytes, pattern: str or bytes):
    return bool(re.search(pattern, obj))


@query_predicate
def is_none(obj: Any):
    return obj is None


@query_predicate
def is_not_none(obj: Any):
    return obj is not None


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


def _kwarg_preds(kwargs: Mapping, getter: Callable) -> Iterator[Callable]:
    for key, value in kwargs.items():
        key_path, operation_name = split_key(key)
        filter_pred = _query_map[operation_name]
        yield filter_pred(getter, key_path, value)


def q_attrs_all(**kwargs) -> Callable:
    return q_all(*_kwarg_preds(kwargs, retrieve_attr))


def q_attrs_any(**kwargs) -> Callable:
    return q_any(*_kwarg_preds(kwargs, retrieve_attr))


def q_attrs_not_any(**kwargs) -> Callable:
    return q_not(q_any(*_kwarg_preds(kwargs, retrieve_attr)))


def q_items_all(**kwargs) -> Callable:
    return q_all(*_kwarg_preds(kwargs, retrieve_item))


def q_items_any(**kwargs) -> Callable:
    return q_any(*_kwarg_preds(kwargs, retrieve_item))


def q_items_not_any(**kwargs) -> Callable:
    return q_not(q_any(*_kwarg_preds(kwargs, retrieve_item)))


q_attrs = q_attrs_all
q_items = q_items_all
