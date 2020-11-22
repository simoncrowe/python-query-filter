from abc import ABC, abstractmethod
from typing import Any, Hashable, Iterable

def retrieve_attr(obj, keys):
    pass

def retrive_item(obj, keys):
    pass


class Predicate(ABC):

    def __init__(keys: Iterable[Hashable], criteria: Any):
        self._keys = keys
        self._criteria = criteria

    def __call__(obj: Any, attrs: bool) -> bool:
        if attrs:
            evaluated_obj = retrieve_attr(obj, self._keys)
        else:
            evaluated_obj = retrieve_item(obj, self._keys)

        if not evaluated_obj:
            return False

        return evaluate(evaluated_obj)

    @abstractmethod
    def evaluate(obj: Any, criteria: Any) -> bool:
        pass

