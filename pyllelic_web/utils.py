"""Utility functions for pyllelic-web"""

from functools import wraps
from typing import Any, Callable


def hash_dict(func: Callable[[Any], Any]) -> Callable[[Any], Any]:
    """Transform mutable dictionnary into immutable.
    Useful to be compatible with lru_cache
    See https://stackoverflow.com/questions/6358481/
    """

    class HDict(dict):  # type:ignore[type-arg]
        def __hash__(self) -> int:  # type:ignore[override]
            return hash(frozenset(self.items()))

    @wraps(func)
    def wrapped(*args: Any, **kwargs: Any) -> Any:
        args = tuple([HDict(arg) if isinstance(arg, dict) else arg for arg in args])
        kwargs = {k: HDict(v) if isinstance(v, dict) else v for k, v in kwargs.items()}
        return func(*args, **kwargs)

    return wrapped
