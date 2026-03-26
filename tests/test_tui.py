import pytest

from battui.tui import BatConfApp, Footer, Header, load_config, run_tui

# === UI tests === #


class TestBatConfApp:
    """BatConfApp UI element and basic behaviour tests"""

    @pytest.mark.asyncio
    async def test_app_starts(self) -> None:
        tui = BatConfApp()
        async with tui.run_test() as _:
            assert tui.is_running

    @pytest.mark.asyncio
    async def test_quit(self) -> None:
        """q to quit"""
        tui = BatConfApp()
        async with tui.run_test() as pilot:
            assert tui.is_running
            await pilot.press('q')
            assert not tui.is_running

    @pytest.mark.asyncio
    async def test_header(self) -> None:
        tui = BatConfApp()
        async with tui.run_test() as _:
            assert tui.query_one(Header) is not None

    @pytest.mark.asyncio
    async def test_footer(self) -> None:
        tui = BatConfApp()
        async with tui.run_test() as _:
            assert tui.query_one(Footer) is not None

    @pytest.mark.asyncio
    async def test_welcome_message(self) -> None:
        tui = BatConfApp()
        async with tui.run_test() as _:
            msg = tui.query_one('#welcome-message')
            assert str(msg.render()) == 'Welcome to BatConf TUI'


class TestBatConfAppWithConfig:
    """BatConfApp behaviour when initialised with a config"""

    @pytest.fixture(autouse=True)
    def cfg(self):
        from example.project.conf import CFG

        self.cfg = CFG

    @pytest.mark.asyncio
    async def test_stores_config(self) -> None:
        tui = BatConfApp(config=self.cfg)
        async with tui.run_test() as _:
            assert tui.is_running
            assert tui.config is self.cfg

    @pytest.mark.asyncio
    async def test_config_displayed(self) -> None:
        tui = BatConfApp(config=self.cfg)
        async with tui.run_test() as _:
            config_view = tui.query_one('#config-display')
            assert str(config_view.render()) == str(self.cfg)


# === load_config tests === #


class TestLoadConfig:
    """load_config integration tests"""

    def test_from_module_path(self) -> None:
        """module::attr syntax loads from an installed module"""
        from example.project.conf import CFG

        assert load_config('example.project.conf::CFG') is CFG

    def test_from_file_path(self) -> None:
        """file_path::attr syntax loads from a file on disk"""
        cfg = load_config('example/conf.py::CFG')
        assert cfg is not None
        assert str(cfg)

    def test_bad_file_path_raises_import_error(self) -> None:
        with pytest.raises(
            ImportError, match='Cannot load file: /no/such/conf.py'
        ):
            load_config('/no/such/conf.py::CFG')

    def test_bad_attr_raises_import_error(self) -> None:
        with pytest.raises(
            ImportError, match="Cannot find 'not_CFG' in example/conf.py"
        ):
            load_config('example/conf.py::not_CFG')


# === run_tui tests === #


class TestRunTui:
    """run_tui CLI error handling"""

    def test_bad_config_path_exits_with_error(
        self, capsys: pytest.CaptureFixture
    ) -> None:
        with pytest.raises(SystemExit) as exc_info:
            run_tui(config_path='/no/such/conf.py::CFG')
        assert exc_info.value.code != 0
        assert 'Cannot load file: /no/such/conf.py' in capsys.readouterr().err

    def test_bad_attr_exits_with_error(
        self, capsys: pytest.CaptureFixture
    ) -> None:
        with pytest.raises(SystemExit) as exc_info:
            run_tui(config_path='example/conf.py::not_CFG')
        assert exc_info.value.code != 0
        assert (
            "Cannot find 'not_CFG' in example/conf.py"
            in capsys.readouterr().err
        )
