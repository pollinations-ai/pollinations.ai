import json
import urllib.request
from importlib.metadata import version as get_installed_version
from packaging.version import Version, parse as parse_version

__all__: list[str] = ["get_latest"]

def get_latest() -> None:
    name = "pollinations"
    installed: Version = parse_version(get_installed_version(name))

    with urllib.request.urlopen(f"https://pypi.org/pypi/{name}/json", timeout=3) as res:
        data = json.load(res)
        latest: Version = parse_version(data["info"]["version"])

    if (installed.major, installed.minor) != (latest.major, latest.minor):
        raise RuntimeError(
            f"Pollinations Version {installed} is outdated. "
            f"Latest is {latest}. Update with:\n\n    pip install -U {name}"
        )
