from unittest import TestCase
from unittest.mock import Mock, create_autospec, patch

from ..tui import BatConfApp, load_config, run_tui
from ..types import BatConfConfig

SRC = 'battui.tui'


class LoadConfigTests(TestCase):
    """Unit tests for load_config"""

    @patch(f'{SRC}.import_module', autospec=True)
    def test_module_path_imports_module(t, import_module: Mock) -> None:
        load_config('some.module::CFG')
        import_module.assert_called_once_with('some.module')

    @patch(f'{SRC}.import_module', autospec=True)
    def test_module_path_returns_named_attribute(t, import_module: Mock) -> None:
        result = load_config('some.module::CFG')
        t.assertIs(result, import_module.return_value.CFG)

    @patch(f'{SRC}.spec_from_file_location', autospec=True)
    def test_file_path_loads_from_file(t, spec_from_file_location: Mock) -> None:
        load_config('/some/path/conf.py::CFG')
        spec_from_file_location.assert_called_once_with(
            '_batui_config', '/some/path/conf.py'
        )

    @patch(f'{SRC}.spec_from_file_location', autospec=True)
    @patch(f'{SRC}.module_from_spec', autospec=True)
    def test_file_path_returns_named_attribute(
        t, module_from_spec: Mock,
         spec_from_file_location: Mock,
    ) -> None:
        result = load_config('/some/path/conf.py::CFG')
        spec_from_file_location.assert_called_with(
            '_batui_config', '/some/path/conf.py',
        )
        module = module_from_spec.return_value
        t.assertIs(result, module.CFG)


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

        # Input
        t.config = create_autospec(BatConfConfig)

    def test___init__(t) -> None:
        t.assertEqual(t.tui.title, 'BatConf TUI')

        # Check bound input keys
        t.assertIn(('q', 'quit', 'Quit'), t.tui.BINDINGS)

        with t.subTest('defaults'):
            t.assertIsNone(t.tui.config)

        with t.subTest('parameters'):
            tui = BatConfApp(config=t.config)
            t.assertIs(tui.config, t.config)

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

    def test_compose_with_config(t) -> None:
        tui = BatConfApp(config=t.config)
        widgets = list(tui.compose())

        with t.subTest('renders config display widget'):
            t.Static.assert_called_with(
                content=str(t.config),
                id='config-display',
                markup=False,
            )

        with t.subTest('config display is in the layout'):
            t.assertIn(t.Static.return_value, widgets)


class tuiTests(TestCase):
    """Tests for non-class members of battui.py"""

    @patch(f'{SRC}.BatConfApp', autospec=True)
    @patch(f'{SRC}.sys.argv', ['batui'])
    def test_run_tui(t, BatConfApp: Mock) -> None:
        run_tui()
        BatConfApp.assert_called_once_with(config=None)
        BatConfApp.return_value.run.assert_called_once()

    @patch(f'{SRC}.load_config')
    @patch(f'{SRC}.BatConfApp', autospec=True)
    def test_run_tui_with_config_path(t, BatConfApp: Mock, load_config: Mock) -> None:
        run_tui(config_path='some.module.CFG')
        load_config.assert_called_once_with('some.module.CFG')
        BatConfApp.assert_called_once_with(config=load_config.return_value)
        BatConfApp.return_value.run.assert_called_once()

    @patch(f'{SRC}.load_config')
    @patch(f'{SRC}.BatConfApp', autospec=True)
    @patch(f'{SRC}.sys.argv', ['batui', 'some.module.CFG'])
    def test_run_tui_reads_config_path_from_argv(t, BatConfApp: Mock, load_config: Mock) -> None:
        run_tui()
        load_config.assert_called_once_with('some.module.CFG')
        BatConfApp.assert_called_once_with(config=load_config.return_value)
