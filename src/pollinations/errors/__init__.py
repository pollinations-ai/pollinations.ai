from .empty_file_error import EmptyFileError
from .failed_to_stream import FailedToStreamError
from .failed_to_transcribe import FailedToTranscribeError
from .file_not_found import FileNotFoundError
from .improper_permissions import ImproperPermissionsError
from .invalid_or_unkown_prompt import InvalidOrUnknownPromptError
from .not_a_file import NotAFileError

__all__: list[str] = [
    "EmptyFileError",
    "FailedToStreamError",
    "FailedToTranscribeError",
    "FileNotFoundError",
    "ImproperPermissionsError",
    "InvalidOrUnknownPromptError",
    "NotAFileError",
]
