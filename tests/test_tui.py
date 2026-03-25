import pytest

from battui.tui import BatConfApp, Footer, Header, load_config


@pytest.mark.asyncio
async def test_app_starts() -> None:
    """Test that the app starts, and welcome message is present"""

    tui = BatConfApp()
    async with tui.run_test() as _:
        assert tui.is_running


@pytest.mark.asyncio
async def test_quit() -> None:
    """q to quit"""

    tui = BatConfApp()
    async with tui.run_test() as pilot:
        assert tui.is_running
        await pilot.press('q')
        assert not tui.is_running


@pytest.mark.asyncio
async def test_header() -> None:
    tui = BatConfApp()
    async with tui.run_test() as _:
        header = tui.query_one(Header)
        # Not much to actually check on the default header
        assert header is not None


@pytest.mark.asyncio
async def test_welcome_message() -> None:
    tui = BatConfApp()
    async with tui.run_test() as _:
        assert tui.is_running
        # check that message is in the DOM
        msg = tui.query_one('#welcome-message')
        assert str(msg.render()) == 'Welcome to BatConf TUI'


@pytest.mark.asyncio
async def test_footer() -> None:
    tui = BatConfApp()
    async with tui.run_test() as _:
        footer = tui.query_one(Footer)
        assert footer is not None


# --- Config loading integration tests ---

def test_load_config_returns_configuration() -> None:
    """load_config with a dotted path returns the object at that path"""
    from example.project.conf import CFG

    cfg = load_config('example.project.conf.CFG')

    assert cfg is CFG


@pytest.mark.asyncio
async def test_app_accepts_config() -> None:
    """BatConfApp stores the config object passed at init"""
    from example.project.conf import CFG

    tui = BatConfApp(config=CFG)

    async with tui.run_test() as _:
        assert tui.is_running
        assert tui.config is CFG


@pytest.mark.asyncio
async def test_config_displayed() -> None:
    """BatConfApp displays the config's string representation"""
    from example.project.conf import CFG

    tui = BatConfApp(config=CFG)

    async with tui.run_test() as _:
        config_view = tui.query_one('#config-display')
        assert str(config_view.render()) == str(CFG)
