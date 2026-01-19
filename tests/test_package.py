from __future__ import annotations

import importlib.metadata

import batconf_tui as m


def test_version():
    assert importlib.metadata.version('batconf_tui') == m.__version__
