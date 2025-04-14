from __future__ import annotations

from pollinations._types import List, Union, Dict, Any, Info
from pollinations.utils._models import text_models, image_models


__all__ = ["text_models", "image_models", "Model"]


class Model:
    def __init__(self, data: Union[Info.TextModel, Info.ImageModel, Dict[str, Any]]):
        self._data = dict(data)

        for key, value in self._data.items():
            setattr(self, key, value)

    def __getattr__(self, item):
        return self._data.get(item, None)

    def __str__(self):
        args = ", ".join(f"{k}={repr(v)}" for k, v in self._data.items())
        return f"Model({args})"

    def info(self) -> Info.TextModel | Info.ImageModel:
        return self._data

    __repr__ = __str__

    def to_dict(self) -> Dict[str, Any]:
        return dict(self._data)

    @classmethod
    def from_text(cls) -> List[Model]:
        return [cls(model) for model in text_models()]

    @classmethod
    def from_image(cls) -> List[Model]:
        return [cls(model) for model in image_models()]
