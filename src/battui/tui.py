import sys
from importlib import import_module
from importlib.util import module_from_spec, spec_from_file_location
from sys import argv, exit
from typing import ClassVar

from textual.app import App, BindingType, ComposeResult
from textual.widgets import Footer, Header, Static

from .types import BatConfConfig


def _load_module_from_file(module_path: str):
    """Load a Python module from a file path.

    Parameters
    ----------
    module_path : str
        Absolute or relative path to the ``.py`` file.

    Returns
    -------
    types.ModuleType
        The loaded module.

    Raises
    ------
    ImportError
        If the file cannot be found or the spec cannot be created.
    """
    spec = spec_from_file_location('_batui_config', module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f'Cannot load file: {module_path}')
    module = module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except FileNotFoundError as err:
        raise ImportError(f'Cannot load file: {module_path}') from err
    return module


def _load_module_from_module_path(module_path: str):
    """Load a Python module by its dotted module path.

    Parameters
    ----------
    module_path : str
        Dotted module path, e.g. ``'some.module'``.

    Returns
    -------
    types.ModuleType
        The imported module.
    """
    return import_module(module_path)


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

    Raises
    ------
    ImportError
        If the module or file cannot be loaded, or the named attribute does
        not exist.
    """
    module_path, attr = path.split('::')
    if '/' in module_path or module_path.endswith('.py'):
        module = _load_module_from_file(module_path)
    else:
        module = _load_module_from_module_path(module_path)
    try:
        return getattr(module, attr)
    except AttributeError:
        raise ImportError(f"Cannot find '{attr}' in {module_path}")


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
            yield Static(
                content=str(self.config), id='config-display', markup=False
            )
        else:
            yield Static(
                content='Welcome to BatConf TUI', id='welcome-message'
            )
        yield Footer()


def run_tui(config_path: str | None = None) -> None:
    if config_path is None and len(argv) > 1:
        config_path = argv[1]
    try:
        config = load_config(config_path) if config_path else None
    except ImportError as e:
        sys.stderr.write(f'Error: {e}\n')
        exit(1)
    tui = BatConfApp(config=config)
    tui.run()
