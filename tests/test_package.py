from __future__ import annotations

import importlib.metadata

import battui as m


def test_version():
    assert importlib.metadata.version('batconf-tui') == m.__version__
