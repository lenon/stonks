# stonks

This repo contains a Python project that I use to keep track of my investments
portfolio in the Brazilian stock market. I wrote it in Python 3 using Pandas for
data analysis. The goal was to replace a complicated Excel spreadsheet I was
using.

Feel free to use the code as you like, but please keep in mind that there is no
guarantee that it is 100% correct or will work for all cases.

## Requirements

* [pyenv][pyenv-instructions] to switch to the correct Python version.
* [Poetry][poetry-instructions] to install dependencies.

## Installation

Clone the repo:

```
git clone git@github.com:lenon/stonks.git && cd stonks
```

Install the correct Python with pyenv:

```
pyenv install
```

And then install dependencies with Poetry:

```
poetry install
```

## Usage

All confirmations, trades and other corporate actions must be filled in an Excel
spreadsheet. There's an example under `tests/fixtures/br-sample.xlsx`:

```
cp tests/fixtures/br-sample.xlsx data/br.xlsx
```

After filling in all information, you can calculate your current portfolio with
the following command:

```
poetry run python -m stonks data/br.xlsx
```

The result will be saved in a new file named `data/br-positions.xlsx`.

[pyenv-instructions]: https://github.com/pyenv/pyenv#installation
[poetry-instructions]: https://python-poetry.org/docs/#installation
