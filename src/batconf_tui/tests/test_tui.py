from unittest import TestCase
from unittest.mock import patch, Mock

from ..tui import BatConfApp, Static, run_tui


SRC = 'batconf_tui.tui'


class BatConfAppTests(TestCase):

    def test___init__(t) -> None:
        tui = BatConfApp()

        t.assertEqual(tui.title, "BatConfApp")

        # Check bound input keys
        t.assertIn(('q', 'quit', 'Quit'), tui.BINDINGS)

    def test_compose(t) -> None:
       tui = BatConfApp()
       widgets: dict[str, Static] = {
           widget.id: widget
           for widget in tui.compose()
       }
       welcome = widgets['welcome-message']
       t.assertEqual('Welcome to BatConf TUI', welcome.render())


class tuiTests(TestCase):

    @patch(f'{SRC}.BatConfApp', autospec=True)
    def test_run_tui(t, BatConfApp: Mock):
        run_tui()
        BatConfApp.assert_called_once()
        BatConfApp.return_value.run.assert_called_once()
