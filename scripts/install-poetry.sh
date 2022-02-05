#!/usr/bin/env bash
set -euxo pipefail

poetry_dir=~/.local/share/pypoetry
poetry_exe=~/.local/bin/poetry

if [[ -d "$poetry_dir" && -x "$poetry_exe" ]]; then
    # poetry installation folder restored from cache, just add to path
    echo ~/.local/bin >>"$GITHUB_PATH"
else
    curl --silent \
        --show-error \
        --location https://install.python-poetry.org \
        --output poetry-installer.py

    python poetry-installer.py --yes --version "$POETRY_VERSION"
fi

poetry --version
