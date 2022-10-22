from typing import Any, Callable, Iterable, Union

from query_filter.query import ObjNotFound, Query, retrieve_value


def _ensure_callable(obj: Union[Callable, Query]):
    if callable(obj):
        return obj

    def truthy_pred(item: Any):
        try:
            return retrieve_value(item, *obj)
        except ObjNotFound:
            return False

    return truthy_pred


def q_filter_any(objects: Iterable, *preds) -> Iterable[Any]:
    def main_predicate(item):
        return any(_ensure_callable(pred)(item) for pred in preds)

    return filter(main_predicate, objects)


def q_filter_not_any(objects: Iterable, *preds) -> Iterable[Any]:
    def main_predicate(item):
        return not any(_ensure_callable(pred)(item) for pred in preds)

    return filter(main_predicate, objects)


def q_filter_all(objects: Iterable, *preds) -> Iterable[Any]:
    def main_predicate(item):
        return all(_ensure_callable(pred)(item) for pred in preds)

    return filter(main_predicate, objects)


q_filter = q_filter_all


def q_all(*preds: Callable) -> Callable:
    def all_pred(obj: Any):
        return all(_ensure_callable(pred)(obj) for pred in preds)
    return all_pred


def q_any(*preds: Callable) -> Callable:
    def any_pred(obj: Any):
        return any(_ensure_callable(pred)(obj) for pred in preds)
    return any_pred


def q_not(pred: Callable) -> Callable:
    def not_pred(obj: Any):
        return not _ensure_callable(pred)(obj)
    return not_pred
