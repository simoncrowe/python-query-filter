from copy import deepcopy
from typing import Iterable


def _simple_keywords_predicate(filter_kwargs: dict):

    def predicate(item):
        for key, value in filter_kwargs.items():

            if key not in item or item[key] != value:
                return False

        return True

    return predicate


def item_filter(items: Iterable, *predicates, **kwargs):
    items_copy = deepcopy(items)
    
    kwargs_predicate = _simple_keywords_predicate(kwargs)

    def main_predicate(item):
        if not kwargs_predicate(item):
            return False

        return all(predicate(item, attrs=False) for predicate in predicates)
    
    return filter(main_predicate, items_copy)
