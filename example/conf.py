from collections.abc import Sequence

# === Configuration Schema === #
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from batconf.manager import ConfigProtocol, Configuration
from batconf.source import SourceInterface, SourceList
from batconf.sources.argparse import Namespace, NamespaceConfig

# from batconf.sources.args import CliArgsConfig, Namespace
from batconf.sources.env import EnvConfig
from batconf.sources.ini import IniConfig


@dataclass
class MyClientConfig:
    key1: str
    key2: str = 'KEY2_DEFAULT'


@dataclass
class SubmoduleConfigSchema:
    client: MyClientConfig


@dataclass
class ClientConfigurationsSchema:
    clientA: MyClientConfig
    clientB: MyClientConfig


@dataclass
class ProjectConfigSchema:
    submodule: SubmoduleConfigSchema
    clients: ClientConfigurationsSchema


# Get the absolute path to the test config.yaml file
_example_project_dir = Path(__file__).parent
CONFIG_FILE_NAME = (_example_project_dir / 'config.ini').resolve()


def get_config(
    config_class: ConfigProtocol | Any = ProjectConfigSchema,
    cfg_path: str = 'project',
    cli_args: Namespace | None = None,
    config_file: SourceInterface | None = None,
    config_file_name: str = str(CONFIG_FILE_NAME),
    config_env: str | None = None,
) -> Configuration:
    """Example get_config function

    This function builds a :class:`SouceList`, which defines the configuration
    sources and lookup order.

    :param config_class: python builtin dataclass
    of type dataclass[dataclass | str].
    Type-hint includes :class:`Any` because mypy does not currently recognize
    the dataclass produced by @dataclass as satisfying the ConfigProtocol.
    :param cli_args: :class:`Namespace` provided by python's builtin argparse
    :param config_file:
    :param config_file_name:
    :param config_env: Environment id string, ex: 'dev', 'staging', 'yourname'
    used by some sources such as :class:`YamlConfig` to
    :return: A batconf :class:`Configuration` instance, used to access config
    values from the :class:`SourceList` using the config_class tree
    or module namespace (these should™ match).
    """

    # Build a prioritized config source list
    config_sources: Sequence[SourceInterface | None] = [
        NamespaceConfig(cli_args) if cli_args else None,
        EnvConfig(),
        (
            config_file
            if config_file
            else IniConfig(config_file_name, config_env=config_env)
        ),
    ]

    source_list = SourceList(config_sources)

    return Configuration(source_list, config_class, path=cfg_path)


CFG = get_config()
