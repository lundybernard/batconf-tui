# batconf-tui

[![Actions Status][actions-badge]][actions-link]
[![Documentation Status][rtd-badge]][rtd-link]

[![PyPI version][pypi-version]][pypi-link]
[![Conda-Forge][conda-badge]][conda-link]
[![PyPI platforms][pypi-platforms]][pypi-link]

[![GitHub Discussion][github-discussions-badge]][github-discussions-link]

[![Coverage][coverage-badge]][coverage-link]

<!-- SPHINX-START -->

A Terminal User Interface for exploring [batconf](https://github.com/lundybernard/batconf) configuration in your projects.

## Overview

`batconf-tui` lets you interactively browse the configuration tree of a batconf-managed project — viewing resolved values, their sources (CLI args, environment variables, config files), and the full schema hierarchy.

## Installation

```bash
pip install batconf-tui
```

## Usage

```bash
batui
```

This launches the TUI. Press `q` to quit.

## Development

### Setup

```bash
pip install -e ".[dev]"
```

### Running tests

```bash
# All tests
pytest

# With coverage
pytest --cov=battui
```

Tests are organized in two layers:

- `tests/` — end-to-end and integration tests
- `src/battui/tests/` — isolated unit tests

An example batconf project for manual testing is provided in `tests/example/`.

### Nox sessions

```bash
nox -l          # list available sessions
nox -s tests    # run tests
```

<!-- SPHINX-END -->

<!-- prettier-ignore-start -->
[actions-badge]:            https://github.com/lundybernard/batconf-tui/workflows/CI/badge.svg
[actions-link]:             https://github.com/lundybernard/batconf-tui/actions
[conda-badge]:              https://img.shields.io/conda/vn/conda-forge/batconf-tui
[conda-link]:               https://github.com/conda-forge/batconf-tui-feedstock
[github-discussions-badge]: https://img.shields.io/static/v1?label=Discussions&message=Ask&color=blue&logo=github
[github-discussions-link]:  https://github.com/lundybernard/batconf-tui/discussions
[pypi-link]:                https://pypi.org/project/batconf-tui/
[pypi-platforms]:           https://img.shields.io/pypi/pyversions/batconf-tui
[pypi-version]:             https://img.shields.io/pypi/v/batconf-tui
[rtd-badge]:                https://readthedocs.org/projects/batconf-tui/badge/?version=latest
[rtd-link]:                 https://batconf-tui.readthedocs.io/en/latest/?badge=latest
[coverage-badge]:           https://codecov.io/github/lundybernard/batconf-tui/branch/main/graph/badge.svg
[coverage-link]:            https://codecov.io/github/lundybernard/batconf-tui

<!-- prettier-ignore-end -->
