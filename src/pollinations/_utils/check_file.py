from ..types import Filename, Args, Kwargs
from ..errors import (
    EmptyFileError,
    FileNotFoundError,
    ImproperPermissionsError,
    NotAFileError,
)

import os

__all__: list[str] = ["_check_file"]


def _check_file(file: Filename, *args: Args, **kwargs: Kwargs) -> bool:
    if not os.path.exists(file):
        raise FileNotFoundError(f"{FileNotFoundError.DefaultMessage[:-1]} | {file}")
    if not os.path.isfile(file):
        raise NotAFileError(f"{NotAFileError.DefaultMessage[:-1]} | {file}")
    if not os.access(file, os.R_OK):
        raise ImproperPermissionsError(f"{ImproperPermissionsError.DefaultMessage[:-1]} | {file}")
    if os.path.getsize(file) == 0:
        raise EmptyFileError(f"{EmptyFileError.DefaultMessage[:-1]} | {file}")

    return True
