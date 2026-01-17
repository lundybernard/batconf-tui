import pytest
from batconf_tui.tui import BatConfApp


@pytest.mark.asyncio
async def test_app_starts() -> None:
    """Test that the app starts, and welcome message is present"""

    tui = BatConfApp()
    async with tui.run_test() as _:
        # check that message is in the DOM
        msg = app.query_one("#welcome-message")
        assert msg.renderable == 'Welcome to BatConf TUI!'


@pytest.mark.asyncio
async def test_quit() -> None:
    """q to quit"""

    tui = BatConfApp()
    async with tui.run_tests as pilot:
        await pilot.press("q")
        assert not app.is_running
