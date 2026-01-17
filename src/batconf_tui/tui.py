from textual.app import App, ComposeResult
from textual.widgets import Static


class BatConfApp(App[None]):
    """A Terminal User Interface for BatConf"""
    BINDINGS = [('q', 'quit', 'Quit'),]

    def compose(self) -> ComposeResult:
        yield Static('Welcome to BatConf TUI', id='welcome-message')


def run_tui() -> None:
    tui = BatConfApp()
    tui.run()
