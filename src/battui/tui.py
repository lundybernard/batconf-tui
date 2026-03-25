import importlib
import sys
from typing import ClassVar

from textual.app import App, BindingType, ComposeResult
from textual.widgets import Footer, Header, Static

from .types import BatConfConfig


def load_config(dotted_path: str) -> BatConfConfig:
    """Import and return a batconf Configuration from a dotted path.

    Example: load_config('project.conf.CFG')
    """
    module_path, attr = dotted_path.rsplit('.', 1)
    module = importlib.import_module(module_path)
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
    if config_path is None and len(sys.argv) > 1:
        config_path = sys.argv[1]
    config = load_config(config_path) if config_path else None
    tui = BatConfApp(config=config)
    tui.run()
