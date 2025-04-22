from typing import Any, Self

__all__: list[str] = ["BaseClass"]


class BaseClass:
    def __repr__(self: Self) -> str:
        def fmt(val: Any) -> str:
            match val:
                case str() if len(val) > 30:
                    return repr(val[:27] + "...")
                case str():
                    return repr(val)
                case bytes() if len(val) > 30:
                    return repr(val[:27] + b"...")
                case list() if len(val) > 3:
                    return f"[{', '.join(fmt(v) for v in val[:3])}, ...]"
                case list():
                    return f"[{', '.join(fmt(v) for v in val)}]"
                case dict() if len(val) > 3:
                    items = ", ".join(
                        f"{fmt(k)}: {fmt(v)}" for k, v in list(val.items())[:3]
                    )
                    return f"{{{items}, ...}}"
                case dict():
                    items = ", ".join(
                        f"{fmt(k)}: {fmt(v)}" for k, v in val.items()
                    )
                    return f"{{{items}}}"
                case tuple() if len(val) > 3:
                    return f"({', '.join(fmt(v) for v in val[:3])}, ...)"
                case tuple():
                    return f"({', '.join(fmt(v) for v in val)})"
                case set() | frozenset() if len(val) > 3:
                    return f"{{{', '.join(fmt(v) for v in sorted(val)[:3])}, ...}}"
                case set() | frozenset():
                    return f"{{{', '.join(fmt(v) for v in sorted(val))}}}"
                case float():
                    return f"{val:.4g}"
                case int() | bool() | None:
                    return repr(val)
                case _:
                    return repr(val)

        public_attrs = {
            k: v for k, v in vars(self).items() if not k.startswith("_")
        }
        cls_name = self.__class__.__name__
        if not public_attrs:
            return f"{cls_name}()"
        body = ", ".join(
            f"{k}={fmt(v)}" for k, v in sorted(public_attrs.items())
        )
        return f"{cls_name}({body})"

    def __str__(self: Self) -> str:
        return self.__repr__()
