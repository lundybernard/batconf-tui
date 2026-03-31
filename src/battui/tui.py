import sys
from functools import cached_property
from importlib import import_module
from importlib.abc import Loader
from importlib.machinery import ModuleSpec
from importlib.util import module_from_spec, spec_from_file_location
from sys import argv
from types import ModuleType
from typing import ClassVar, cast

from textual.app import App, BindingType, ComposeResult
from textual.widgets import Footer, Header, Static

from .types import BatConfConfig


class ConfigLoader:
    """Load a batconf config object from a ``module::Attr`` path string.

    Instantiate with a ``config_path`` and access ``.config`` to retrieve
    the object.  Intermediate properties (``file_path``, ``module_path``,
    ``spec``, ``loader``, ``module``) are cached on first access and can be
    inspected individually.

    Parameters
    ----------
    config_path : str
        Location of the config object in ``path::Attr`` format.  Two forms
        are accepted:

        - ``'some.module::AttrName'`` — dotted module path.
        - ``'/path/to/conf.py::AttrName'`` — file path (contains ``/`` or
          ends with ``.py``).
    """

    def __init__(self, config_path: str) -> None:
        self.config_path = config_path
        self._path: str = self.config_path.split('::')[0]
        self.attr: str = self.config_path.split('::')[1]

    @cached_property
    def file_path(self) -> str | None:
        """The file path component, or ``None`` if this is a module path."""
        if '/' in self._path or self._path.endswith('.py'):
            return self._path
        return None

    @cached_property
    def module_path(self) -> str | None:
        """The dotted module path, or ``None`` if this is a file path.

        Returns ``None`` for strings that are not valid dotted identifiers.
        """
        if all(part.isidentifier() for part in self._path.split('.')):
            return self._path
        return None

    @cached_property
    def spec(self) -> ModuleSpec:
        """The ``ModuleSpec`` for the file path.

        Raises
        ------
        ImportError
            If ``spec_from_file_location`` cannot produce a spec (e.g. the
            file extension is not recognised).
        """
        spec = spec_from_file_location('_batui_config', self.file_path)
        if spec is None:
            msg = f'Cannot load file: {self.file_path}'
            raise ImportError(msg)
        return spec

    @cached_property
    def loader(self) -> Loader:
        """The file loader extracted from ``spec``."""
        loader = self.spec.loader
        if loader is None:
            msg = f'Cannot load file: {self.file_path}'
            raise ImportError(msg)
        return loader

    @cached_property
    def module(self) -> ModuleType:
        """The imported module, loaded via the appropriate strategy.

        Raises
        ------
        ImportError
            If the file does not exist on disk, or if the module cannot be
            imported.
        """
        if self.module_path:
            return import_module(self.module_path)

        # Load from a .py file
        module = module_from_spec(self.spec)
        sys.modules[self.spec.name] = module
        try:
            self.loader.exec_module(module)
        except FileNotFoundError as err:
            sys.modules.pop(self.spec.name, None)
            msg = f'Cannot load file: {self.file_path}'
            raise ImportError(msg) from err
        return module

    @cached_property
    def config(self) -> BatConfConfig:
        """The config object at ``attr`` on the loaded module.

        Raises
        ------
        ImportError
            If ``attr`` does not exist on the module.
        """
        try:
            return cast('BatConfConfig', getattr(self.module, self.attr))
        except AttributeError as err:
            msg = (
                f"Cannot find '{self.attr}'"
                f' in {self.file_path or self.module_path}'
            )
            raise ImportError(msg) from err


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
        config = ConfigLoader(config_path).config if config_path else None
    except ImportError as e:
        sys.stderr.write(f'Error: {e}\n')
        exit(1)
    tui = BatConfApp(config=config)
    tui.run()
