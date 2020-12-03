from typing import Any, Callable, Iterable


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
