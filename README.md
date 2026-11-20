# stonks

This repository contains a Python project that I developed to manage my investment portfolio in the
Brazilian stock market. The project uses Pandas for data analysis and is intended to replace the
complex Excel spreadsheet I previously used.

The code is available for anyone to use, but please note that I cannot guarantee its accuracy. Use
it at your own risk.

## Requirements

* [uv][uv-instructions] to install Python and dependencies.

## Installation

Clone the repo:

```
git clone git@github.com:lenon/stonks.git && cd stonks
```

Install the correct Python and dependencies with uv:

```
uv sync
```

Run commands inside the project environment with `uv run`, for example:

```
uv run pytest
```

[uv-instructions]: https://docs.astral.sh/uv/getting-started/installation/
