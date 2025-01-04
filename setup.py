from setuptools import setup, find_packages
from pathlib import Path

path_absolute: Path = Path(__file__).parent.absolute()

with open(f"{path_absolute}/pollinations/__init__.py", "r") as file:
    for line in file.readlines():
        if line.startswith("__version__"):
            version = line.split("=")[1].strip()[1:-1]
            break

setup(
    name="pollinations.ai",
    version=version,
    description="pollinations.ai | Free AI Text & Image Generation",
    long_description=Path(f"{path_absolute}/README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    url="https://pollinations.ai/",
    author="git.pollinations.ai",
    author_email="git.pollinations.ai@gmail.com",
    license="MIT",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Development Status :: 4 - Beta",
        "Natural Language :: English"
    ],
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    python_requires=">=3.7",
    keywords=["pollinations", "pollinations.ai", "pollinations-ai", "pollinations_ai", "ai", "api", "sdk", "wrapper", "free"],
    install_requires=[
        "chardet"
    ],
    project_urls={
        "Website": "https://pollinations.ai/",
        "Discord": "https://discord.gg/8HqSRhJVxn",
        "Github": "https://github.com/pollinations",
        "YouTube": "https://www.youtube.com/channel/UCk4yKnLnYfyUmCCbDzOZOug",
        "Instagram": "https://instagram.com/pollinations_ai",
        "Twitter": "https://twitter.com/pollinations_ai",
    }
) 
