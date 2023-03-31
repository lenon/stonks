# stonks

This repository includes a Python project that I developed to manage my
investment portfolio in the Brazilian stock market. The project is written in
Python 3 and utilizes Pandas for data analysis. Its primary purpose is to
replace the complex Excel spreadsheet that I previously used.

While the code is available for your use, it is important to note that I cannot
guarantee its accuracy. Please use it at your own discretion.

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
