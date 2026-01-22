import pytest

from battui.tui import BatConfApp


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
async def test_welcome_message() -> None:
    tui = BatConfApp()
    async with tui.run_test() as _:
        assert tui.is_running
        # check that message is in the DOM
        msg = tui.query_one('#welcome-message')
        assert str(msg.render()) == 'Welcome to BatConf TUI'
