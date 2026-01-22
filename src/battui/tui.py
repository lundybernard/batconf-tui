from typing import ClassVar

from textual.app import App, ComposeResult
from textual.binding import BindingType
from textual.widgets import Static


class BatConfApp(App[None]):
    """A Terminal User Interface for BatConf"""

    BINDINGS: ClassVar[list[BindingType]] = [
        ('q', 'quit', 'Quit'),
    ]

    def compose(self) -> ComposeResult:
        yield Static('Welcome to BatConf TUI', id='welcome-message')


def run_tui() -> None:
    tui = BatConfApp()
    tui.run()
