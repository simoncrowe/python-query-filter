from typing import Any, Callable, Iterable


def query_predicate(predicate: Callable):
    """
    Decorates functions that evaluate something against some criteria.

    The immediate output is a function that accepts the criteria by which
    an object is to be evaluated and the means of getting this object from
    a "root" object. This funtion returns a predicate that evaluates any
    "root" object accoring to these criteria, using the decorated function.
    """
    def pred_maker(criteria: Any, getter: Callable, keys: Iterable[Any]):

        def pred(obj: Any):
            evaluated = getter(obj, *keys)
            if evaluated is None:
                return False
            return predicate(evaluated, criteria)

        return pred

    return pred_maker


@query_predicate
def lt(evaluated: Any, criteria: Any):
    return evaluated < criteria


@query_predicate
def lte(obj: Any, criteria: Any):
    return obj <= criteria


@query_predicate
def eq(obj: Any, criteria: Any):
    return obj == criteria


@query_predicate
def ne(obj: Any, criteria: Any):
    return obj != criteria


@query_predicate
def gt(obj: Any, criteria: Any):
    return obj > criteria


@query_predicate
def gte(obj: Any, criteria: Any):
    return obj >= criteria


@query_predicate
def is_in(obj: Any, criteria: Any):
    return obj in criteria


@query_predicate
def contains(obj: Any, criteria: Any):
    return criteria in obj


@query_predicate
def _is(obj: Any, criteria: Any):
    return obj is criteria


@query_predicate
def _is_not(obj: Any, criteria: Any):
    return obj is not criteria
