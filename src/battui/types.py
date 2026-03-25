from typing import Any, Protocol


class BatConfConfig(Protocol):
    """Interface required by battui from a batconf config object.

    Both batconf.manager.Configuration and batconf.lib.ConfigSingleton
    satisfy this interface. Extend as the TUI discovers new requirements.
    """

    @property
    def _path(self) -> str: ...

    def __getattr__(self, name: str) -> Any: ...
