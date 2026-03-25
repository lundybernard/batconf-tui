import io
from unittest import TestCase
from unittest.mock import Mock, create_autospec, patch

from ..tui import BatConfApp, load_config, run_tui
from ..types import BatConfConfig

SRC = 'battui.tui'


class LoadConfigTests(TestCase):
    """Unit tests for load_config"""

    import_module: Mock
    spec_from_file_location: Mock
    module_from_spec: Mock

    def setUp(t) -> None:  # pylint: disable=arguments-renamed
        for target in ('import_module', 'spec_from_file_location', 'module_from_spec'):
            patcher = patch(f'{SRC}.{target}', autospec=True)
            setattr(t, target, patcher.start())
            t.addCleanup(patcher.stop)

        t.module_config_path = 'some.module::CFG'
        t.file_config_path = '/some/path/conf.py::CFG'

    def test_module_path_imports_module(t) -> None:
        load_config(t.module_config_path)
        t.import_module.assert_called_once_with('some.module')
        t.spec_from_file_location.assert_not_called()

    def test_module_path_returns_named_attribute(t) -> None:
        result = load_config(t.module_config_path)
        t.assertIs(result, t.import_module.return_value.CFG)

    def test_file_path_loads_from_file(t) -> None:
        load_config(t.file_config_path)
        t.spec_from_file_location.assert_called_once_with(
            '_batui_config', '/some/path/conf.py'
        )
        t.import_module.assert_not_called()

    def test_file_path_returns_named_attribute(t) -> None:
        result = load_config(t.file_config_path)
        t.module_from_spec.assert_called_once_with(
            t.spec_from_file_location.return_value
        )
        module = t.module_from_spec.return_value
        t.assertIs(result, module.CFG)

    def test_raises_import_error_when_attr_not_found(t) -> None:
        t.import_module.return_value = Mock(spec=[])  # no attributes
        with t.assertRaises(ImportError, msg="Cannot find 'CFG' in some.module"):
            load_config(t.module_config_path)

    def test_file_path_raises_import_error_when_spec_is_none(t) -> None:
        t.spec_from_file_location.return_value = None
        with t.assertRaises(ImportError):
            load_config(t.file_config_path)

    def test_file_path_raises_import_error_when_loader_is_none(t) -> None:
        t.spec_from_file_location.return_value.loader = None
        with t.assertRaises(ImportError):
            load_config(t.file_config_path)

    def test_file_path_raises_import_error_when_file_not_found(t) -> None:
        spec = t.spec_from_file_location.return_value
        spec.loader.exec_module.side_effect = FileNotFoundError
        with t.assertRaises(ImportError):
            load_config(t.file_config_path)


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

    BatConfApp: Mock
    load_config: Mock

    def setUp(t) -> None:  # pylint: disable=arguments-renamed
        for target in ('BatConfApp', 'load_config'):
            patcher = patch(f'{SRC}.{target}', autospec=True)
            setattr(t, target, patcher.start())
            t.addCleanup(patcher.stop)

    @patch(f'{SRC}.argv', ['batui'])
    def test_run_tui(t) -> None:
        run_tui()
        t.load_config.assert_not_called()
        t.BatConfApp.assert_called_once_with(config=None)
        t.BatConfApp.return_value.run.assert_called_once()

    def test_run_tui_with_config_path(t) -> None:
        run_tui(config_path='some.module::CFG')
        t.load_config.assert_called_once_with('some.module::CFG')
        t.BatConfApp.assert_called_once_with(config=t.load_config.return_value)
        t.BatConfApp.return_value.run.assert_called_once()

    @patch(f'{SRC}.argv', ['batui', 'some.module::CFG'])
    def test_run_tui_reads_config_path_from_argv(t) -> None:
        run_tui()
        t.load_config.assert_called_once_with('some.module::CFG')
        t.BatConfApp.assert_called_once_with(config=t.load_config.return_value)

    @patch(f'{SRC}.sys.stderr')
    def test_run_tui_import_error_exits_with_message(t, stderr: Mock) -> None:
        t.load_config.side_effect = ImportError('Cannot load file: /bad/conf.py')
        with t.assertRaises(SystemExit) as ctx:
            run_tui(config_path='/bad/conf.py::CFG')
        t.assertNotEqual(ctx.exception.code, 0)
        stderr.write.assert_called_once_with(
            'Error: Cannot load file: /bad/conf.py\n'
        )
