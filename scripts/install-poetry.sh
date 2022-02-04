#!/usr/bin/env bash
set -euxo pipefail

curl --silent \
    --show-error \
    --location https://install.python-poetry.org \
    --output poetry-installer.py

python poetry-installer.py --yes --version "$POETRY_VERSION"
