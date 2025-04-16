from typing import Final, Dict

from httpx import Timeout

__all__: list[str] = [
    "TEXT_API_URI",
    "IMAGE_API_URI",
    "DEFAULT_TIMEOUT",
    "DEFAULT_MAX_RETRIES",
    "DEFAULT_HEADERS",
]

TEXT_API_URI: Final[str] = "https://text.pollinations.ai/"
IMAGE_API_URI: Final[str] = "https://image.pollinations.ai/"

DEFAULT_TIMEOUT: Final[Timeout] = Timeout(timeout=100, 
                                          connect=5)
DEFAULT_MAX_RETRIES: Final[int] = 3

DEFAULT_HEADERS: Final[Dict[str, str]] = {
    "Accept": "application/json",
    "Content-Type": "application/json",
}
