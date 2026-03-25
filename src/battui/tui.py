from importlib import import_module
from importlib.util import module_from_spec, spec_from_file_location
from sys import argv
from typing import ClassVar

from textual.app import App, BindingType, ComposeResult
from textual.widgets import Footer, Header, Static

from .types import BatConfConfig


def load_config(path: str) -> BatConfConfig:
    """Import and return a batconf config object.

    Parameters
    ----------
    path : str
        Location of the config object in ``module::Attr`` format.
        Two forms are accepted:

        - Module path: ``'some.module::AttrName'`` — imports via
          :func:`importlib.import_module`.
        - File path: ``'/path/to/conf.py::AttrName'`` — loads the file
          directly via :func:`importlib.util.spec_from_file_location`.

    Returns
    -------
    BatConfConfig
        The config object found at the given path.
    """
    module_path, attr = path.split('::')
    if '/' in module_path or module_path.endswith('.py'):
        spec = spec_from_file_location('_batui_config', module_path)
        module = module_from_spec(spec)
        spec.loader.exec_module(module)  # type: ignore[union-attr]
    else:
        module = import_module(module_path)
    return getattr(module, attr)


class BatConfApp(App[None]):
    """A Terminal User Interface for BatConf"""

    TITLE = 'BatConf TUI'

    BINDINGS: ClassVar[list[BindingType]] = [
        ('q', 'quit', 'Quit'),
    ]

    def __init__(self, config: BatConfConfig | None = None) -> None:
        super().__init__()
        self.config = config

    def compose(self) -> ComposeResult:
        yield Header()
        if self.config is not None:
            yield Static(content=str(self.config), id='config-display', markup=False)
        else:
            yield Static(content='Welcome to BatConf TUI', id='welcome-message')
        yield Footer()


def run_tui(config_path: str | None = None) -> None:
    if config_path is None and len(argv) > 1:
        config_path = argv[1]
    config = load_config(config_path) if config_path else None
    tui = BatConfApp(config=config)
    tui.run()
