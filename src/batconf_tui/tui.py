from typing import ClassVar

from textual.app import App, ComposeResult
from textual.widgets import Static


class BatConfApp(App[None]):
    """A Terminal User Interface for BatConf"""

    BINDINGS: ClassVar[list[tuple[str, str, str]]] = [
        ('q', 'quit', 'Quit'),
    ]

    def compose(self) -> ComposeResult:
        yield Static('Welcome to BatConf TUI', id='welcome-message')


def run_tui() -> None:
    tui = BatConfApp()
    tui.run()
