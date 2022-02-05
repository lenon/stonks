#!/usr/bin/env bash
set -euxo pipefail

PYTHON_VERSION=$(cat .python-version)

echo "PYTHON_VERSION=$PYTHON_VERSION" >>"$GITHUB_ENV"
