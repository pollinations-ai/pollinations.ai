import httpx

__all__ = [
    "TEXT_API_URI",
    "IMAGE_API_URI",
    "DEFAULT_TIMEOUT",
    "DEFAULT_MAX_RETRIES",
    "DEFAULT_HEADERS",
]

TEXT_API_URI = "https://text.pollinations.ai/"
IMAGE_API_URI = "https://image.pollinations.ai/"

DEFAULT_TIMEOUT = httpx.Timeout(timeout=100, connect=5)
DEFAULT_MAX_RETRIES = 3

DEFAULT_HEADERS = {"Accept": "application/json", "Content-Type": "application/json"}
