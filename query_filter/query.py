import dataclasses
import enum
import re
from operator import getitem
from typing import Any, Callable, Hashable, Iterable, Iterator


class LookupType(enum.Enum):
    ITEM = 1
    ATTR = 2


@dataclasses.dataclass(frozen=True)
class Lookup:
    lookup_type: LookupType
    key: Hashable


class Query:
    def __init__(self, lookups=()):
        self._lookups = lookups

    def __iter__(self) -> Iterator[Lookup]:
        yield from self._lookups

    def __getattribute__(self, name):
        if name == "_lookups":
            return super().__getattribute__(name)

        new_lookup = Lookup(lookup_type=LookupType.ATTR, key=name)
        return Query(self._lookups + (new_lookup,))

    def __getitem__(self, key):
        new_lookup = Lookup(lookup_type=LookupType.ITEM, key=key)
        return Query(self._lookups + (new_lookup,))

    def __lt__(self, criterion: Any) -> Callable:
        return lt(self, criterion)

    def __le__(self, criterion: Any) -> Callable:
        return lte(self, criterion)

    def __eq__(self, criterion: Any) -> Callable:
        return eq(self, criterion)

    def __ne__(self, criterion: Any) -> Callable:
        return ne(self, criterion)

    def __gt__(self, criterion: Any) -> Callable:
        return gt(self, criterion)

    def __ge__(self, criterion: Any) -> Callable:
        return gte(self, criterion)

    def __invert__(self):
        return negate(self)


def q_is_in(query: Query, container: Any) -> Callable:
    return is_in(query, container)


def q_contains(query: Query, member: Any) -> Callable:
    return contains(query, member)


def q_matches_regex(query: Query, pattern: str) -> Callable:
    return regex(query, pattern)


def q_is(query: Query, criterion: Any) -> Callable:
    return _is(query, criterion)


def q_is_not(query: Query, criterion: Any) -> Callable:
    return _is_not(query, criterion)


def q_is_none(query: Query) -> Callable:
    return is_none(query)


def q_is_not_none(query: Query) -> Callable:
    return is_not_none(query)


class ObjNotFound(Exception):
    """Raised when the requested attr or item is not found."""


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
    to nested "child"

    The immediate output is a function that accepts a sequence of
    lookup data indicating the desired "child" object in a "root" object.
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


def query_criteria(comparer: Callable):
    """
    Like query_predicate, but decorates functions that evaluate
    a "child" object against some criteria.
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


@query_criteria
def lt(evaluated: Any, criterion: Any):
    return evaluated < criterion


@query_criteria
def lte(obj: Any, criterion: Any):
    return obj <= criterion


@query_criteria
def eq(obj: Any, criterion: Any):
    return obj == criterion


@query_criteria
def ne(obj: Any, criterion: Any):
    return obj != criterion


@query_criteria
def gt(obj: Any, criterion: Any):
    return obj > criterion


@query_criteria
def gte(obj: Any, criterion: Any):
    return obj >= criterion


@query_criteria
def is_in(obj: Any, container: Any):
    return obj in container


@query_criteria
def contains(obj: Any, member: Any):
    return member in obj


@query_criteria
def _is(obj: Any, criterion: Any):
    return obj is criterion


@query_criteria
def _is_not(obj: Any, criterion: Any):
    return obj is not criterion


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
def negate(obj: Any):
    return not obj
