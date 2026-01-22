from typing import ClassVar

from textual.app import App, BindingType, ComposeResult
from textual.widgets import Footer, Header, Static


class BatConfApp(App[None]):
    """A Terminal User Interface for BatConf"""

    TITLE = 'BatConf TUI'

    BINDINGS: ClassVar[list[BindingType]] = [
        ('q', 'quit', 'Quit'),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static(content='Welcome to BatConf TUI', id='welcome-message')
        yield Footer()


def run_tui() -> None:
    tui = BatConfApp()
    tui.run()
