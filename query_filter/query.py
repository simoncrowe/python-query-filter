import dataclasses
import enum
import operator
import re
from collections.abc import Container
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

    def __lt__(self, criterion: Any) -> Callable[[Any], bool]:
        return lt(self, criterion)

    def __le__(self, criterion: Any) -> Callable[[Any], bool]:
        return le(self, criterion)

    def __eq__(self, criterion: Any) -> Callable[[Any], bool]:
        return eq(self, criterion)

    def __ne__(self, criterion: Any) -> Callable[[Any], bool]:
        return ne(self, criterion)

    def __gt__(self, criterion: Any) -> Callable[[Any], bool]:
        return gt(self, criterion)

    def __ge__(self, criterion: Any) -> Callable[[Any], bool]:
        return ge(self, criterion)

    def __invert__(self) -> Callable[[Any], bool]:
        return negate(self)


def q_contains(query: Query, item: Any) -> Callable[[Container], bool]:
    return contains(query, item)


def q_is_in(query: Query, container: Container) -> Callable[[Any], bool]:
    return is_in(query, container)


def q_matches_regex(query: Query, pattern: str) -> Callable[[str | bytes], bool]:
    return regex(query, pattern)


def q_is(query: Query, criterion: Any) -> Callable[[Any], bool]:
    return is_(query, criterion)


def q_is_not(query: Query, criterion: Any) -> Callable[[Any], bool]:
    return is_not(query, criterion)


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


lt = query_criteria(operator.lt)
le = query_criteria(operator.le)
eq = query_criteria(operator.eq)
ne = query_criteria(operator.ne)
gt = query_criteria(operator.gt)
ge = query_criteria(operator.ge)
is_ = query_criteria(operator.is_)
is_not = query_criteria(operator.is_not)
contains = query_criteria(operator.contains)


@query_criteria
def is_in(obj: Any, container: Any) -> bool:
    return obj in container


@query_predicate
def negate(obj: Any):
    return not obj


@query_criteria
def regex(obj: str | bytes, pattern: str | bytes):
    return bool(re.search(pattern, obj))
