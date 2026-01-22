from unittest import TestCase
from unittest.mock import Mock, patch

from ..tui import BatConfApp, run_tui

SRC = 'battui.tui'


class BatConfAppTests(TestCase):
    """BatConfApp TUI unit tests"""

    Header: Mock
    Static: Mock
    Footer: Mock

    def setUp(t) -> None:  # pylint: disable=arguments-renamed
        patches = [
            'Header',
            'Static',
            'Footer',
        ]
        for target in patches:
            patcher = patch(f'{SRC}.{target}', autospec=True)
            setattr(t, target, patcher.start())
            t.addCleanup(patcher.stop)

        t.tui = BatConfApp()
        t.widgets = list(t.tui.compose())

    def test___init__(t) -> None:
        t.assertEqual(t.tui.title, 'BatConf TUI')

        # Check bound input keys
        t.assertIn(('q', 'quit', 'Quit'), t.tui.BINDINGS)

    def test_header(t) -> None:
        header = t.widgets[0]
        t.Header.assert_called_once()
        t.assertIs(header, t.Header.return_value)

    def test_test_area(t) -> None:
        text_area = t.widgets[1]
        t.Static.assert_called_with(
            content='Welcome to BatConf TUI',
            id='welcome-message',
        )
        t.assertIs(text_area, t.Static.return_value)

    def test_footer(t) -> None:
        text_area = t.widgets[2]
        t.Footer.assert_called_once()
        t.assertIs(text_area, t.Footer.return_value)


class tuiTests(TestCase):
    """Tests for non-class members of battui.py"""

    @patch(f'{SRC}.BatConfApp', autospec=True)
    def test_run_tui(t, BatConfApp: Mock) -> None:
        run_tui()
        BatConfApp.assert_called_once()
        BatConfApp.return_value.run.assert_called_once()
