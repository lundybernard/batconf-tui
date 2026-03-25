import importlib
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
        yield Static(content='Welcome to BatConf TUI', id='welcome-message')
        yield Footer()


def run_tui() -> None:
    tui = BatConfApp()
    tui.run()
