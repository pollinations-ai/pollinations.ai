FROM mcr.microsoft.com/devcontainers/python:3.11

RUN apt-get update && apt-get install -y \
    curl \
    git \
    && apt-get clean

RUN pip install --upgrade pip && \
    pip install black flake8
