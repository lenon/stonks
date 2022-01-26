from pathlib import Path


def fixture_path(fixture):
    return Path(__file__).parent.joinpath("fixtures", fixture).resolve()
