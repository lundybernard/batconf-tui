from unittest import TestCase

from ..tui import BatConfApp, Static


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
