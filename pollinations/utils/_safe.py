import ast
import inspect
from functools import wraps

from pollinations._types import (
    Any,
    Callable,
    Dict,
    Optional,
    Type,
    TypeVar,
    Union,
    Tuple,
)

__all__ = ["Safe"]

T = TypeVar("T")


class Safe:
    _handlers: Dict[Type[Any], Callable[[Any], Any]] = {}

    @classmethod
    def register(cls, type_: Type[T], handler: Callable[[Any], T]) -> None:
        cls._handlers[type_] = handler

    @staticmethod
    def _try(value: str) -> Any:
        try:
            return ast.literal_eval(value)
        except Exception:
            return value

    def __call__(
        self,
        value: Any,
        to_type: Optional[Type[T]] = None,
        fallback: Optional[T] = None,
    ) -> Optional[T]:
        try:
            if value is None:
                return fallback

            if to_type is None:
                if isinstance(value, (int, float, str, bool)):
                    return value
                if isinstance(value, (list, tuple, dict, set)):
                    return self(value, type(value), fallback)
                return self._try(str(value))

            if to_type in self._handlers:
                return self._handlers[to_type](value)

            if to_type is int:
                if isinstance(value, bool):
                    return int(value)
                return int(float(str(value).strip()))

            if to_type is float:
                if isinstance(value, bool):
                    return float(value)
                return float(str(value).strip())

            if to_type is bool:
                val = str(value).strip().lower()
                if val in ("true", "1", "yes"):
                    return True
                if val in ("false", "0", "no"):
                    return False
                return bool(value)

            if to_type is str:
                return str(value)

            if to_type is list:
                if isinstance(value, str):
                    value = self._try(value)
                items = value if isinstance(value, list) else [value]
                return [self(item, None, fallback) for item in items]

            if to_type is tuple:
                return tuple(self(value, list, fallback))

            if to_type is set:
                return set(self(value, list, fallback))

            if to_type is dict:
                if isinstance(value, str):
                    value = self._try(value)
                if isinstance(value, dict):
                    return {
                        self(k, None, fallback): self(v, None, fallback)
                        for k, v in value.items()
                    }
                return {}

            return to_type(value)

        except Exception:
            return fallback

    @classmethod
    def auto(
        cls, **rules: Union[Type[Any], Tuple[Type[Any], ...], Tuple[Type[Any], Any]]
    ) -> Callable:
        def parse(
            rule: Union[Type[Any], Tuple]
        ) -> Tuple[Union[Type[Any], Tuple[Type[Any], ...]], Any]:
            if isinstance(rule, tuple):
                if len(rule) == 1:
                    return rule[0], None
                *types, fallback = rule
                return types if len(types) > 1 else types[0], fallback
            return rule, None

        def decorator(func: Callable) -> Callable:
            sig = inspect.signature(func)

            @wraps(func)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                bound_args = sig.bind_partial(*args, **kwargs)
                bound_args.apply_defaults()
                safe = cls()

                for arg_name, rule in rules.items():
                    target_type, fallback = parse(rule)

                    if arg_name in bound_args.arguments:
                        val = bound_args.arguments[arg_name]
                        if isinstance(target_type, (list, tuple)):
                            for t in target_type:
                                val = safe(val, t, fallback)
                        else:
                            val = safe(val, target_type, fallback)
                        bound_args.arguments[arg_name] = val

                return func(*bound_args.args, **bound_args.kwargs)

            return wrapper

        return decorator
