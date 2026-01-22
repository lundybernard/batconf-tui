from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from textual.widget import Widget

from unittest import TestCase
from unittest.mock import Mock, patch

from ..tui import BatConfApp, run_tui

SRC = 'battui.tui'


class BatConfAppTests(TestCase):
    """BatConfApp TUI unit tests"""

    def test___init__(t) -> None:
        tui = BatConfApp()

        t.assertEqual(tui.title, 'BatConfApp')

        # Check bound input keys
        t.assertIn(('q', 'quit', 'Quit'), tui.BINDINGS)

    def test_compose(t) -> None:
        tui = BatConfApp()
        widgets: dict[str, Widget] = {
            widget.id: widget
            for widget in tui.compose()
            if widget.id is not None
        }
        welcome = widgets['welcome-message']
        t.assertEqual('Welcome to BatConf TUI', welcome.render())


class tuiTests(TestCase):
    """Tests for non-class members of battui.py"""

    @patch(f'{SRC}.BatConfApp', autospec=True)
    def test_run_tui(t, BatConfApp: Mock) -> None:
        run_tui()
        BatConfApp.assert_called_once()
        BatConfApp.return_value.run.assert_called_once()
