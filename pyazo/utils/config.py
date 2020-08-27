"""pyazo core config loader"""
import os
from collections.abc import Mapping
from contextlib import contextmanager
from glob import glob
from typing import Any, Dict, List
from urllib.parse import urlparse

import yaml
from django.conf import ImproperlyConfigured
from structlog import get_logger

SEARCH_PATHS = [
    "pyazo/utils/default.yml",
    "/etc/pyazo/config.yml",
    "",
] + glob("/etc/pyazo/config.d/*.yml", recursive=True)
LOGGER = get_logger()
ENV_PREFIX = "PYAZO"
ENVIRONMENT = os.getenv(f"{ENV_PREFIX}_ENV", "local")


class ConfigLoader:
    """Search through SEARCH_PATHS and load configuration. Environment variables starting with
    `ENV_PREFIX` are also applied.

    A variable like pyazo_POSTGRESQL__HOST would translate to postgresql.host"""

    loaded_file: List[str] = []

    __config: Dict[Any, Any] = {}
    __sub_dicts = []

    def __init__(self):
        super().__init__()
        base_dir = os.path.realpath(os.path.join(os.path.dirname(__file__), "../.."))
        for path in SEARCH_PATHS:
            # Check if path is relative, and if so join with base_dir
            if not os.path.isabs(path):
                path = os.path.join(base_dir, path)
            if os.path.isfile(path) and os.path.exists(path):
                # Path is an existing file, so we just read it and update our config with it
                self.update_from_file(path)
            elif os.path.isdir(path) and os.path.exists(path):
                # Path is an existing dir, so we try to read the env config from it
                env_paths = [
                    os.path.join(path, ENVIRONMENT + ".yml"),
                    os.path.join(path, ENVIRONMENT + ".env.yml"),
                ]
                for env_file in env_paths:
                    if os.path.isfile(env_file) and os.path.exists(env_file):
                        # Update config with env file
                        self.update_from_file(env_file)
        self.update_from_env()

    @staticmethod
    def merge(root: Dict[Any, Any], updatee: Dict[Any, Any]) -> Dict[Any, Any]:
        """Recursively update dictionary"""
        for key, value in updatee.items():
            if isinstance(value, Mapping):
                root[key] = ConfigLoader.merge(root.get(key, {}), value)
            else:
                if isinstance(value, str):
                    value = ConfigLoader.parse_uri(value)
                root[key] = value
        return root

    @staticmethod
    def parse_uri(value: str) -> str:
        """Parse string values which start with a URI"""
        url = urlparse(value)
        if url.scheme == "env":
            value = os.getenv(url.netloc, url.query)
        return value

    def update_from_file(self, path: str):
        """Update config from file contents"""
        try:
            with open(path) as file:
                try:
                    ConfigLoader.merge(self.__config, yaml.safe_load(file))
                    LOGGER.debug("Loaded config", file=path)
                    self.loaded_file.append(path)
                except yaml.YAMLError as exc:
                    raise ImproperlyConfigured from exc
        except PermissionError as exc:
            LOGGER.warning("Permission denied while reading file", path=path, error=exc)

    def update_from_dict(self, update: Dict[Any, Any]):
        """Update config from dict"""
        self.__config.update(update)

    def update_from_env(self):
        """Check environment variables"""
        outer = {}
        idx = 0
        for key, value in os.environ.items():
            if not key.startswith(ENV_PREFIX):
                continue
            relative_key = key.replace(f"{ENV_PREFIX}_", "").replace("__", ".").lower()
            # Recursively convert path from a.b.c into outer[a][b][c]
            current_obj = outer
            dot_parts = relative_key.split(".")
            for dot_part in dot_parts[:-1]:
                if dot_part not in current_obj:
                    current_obj[dot_part] = {}
                current_obj = current_obj[dot_part]
            current_obj[dot_parts[-1]] = value
            idx += 1
        if idx > 0:
            LOGGER.debug("Loaded environment variables", count=idx)
            ConfigLoader.merge(self.__config, outer)

    @contextmanager
    # pylint: disable=invalid-name
    def cd(self, sub: str):
        """Contextmanager that descends into sub-dict. Can be chained."""
        self.__sub_dicts.append(sub)
        yield
        self.__sub_dicts.pop()

    @property
    def raw(self) -> Dict[Any, Any]:
        """Get raw config dictionary"""
        return self.__config

    # pylint: disable=invalid-name
    def y(self, path: str, default=None, sep=".") -> Any:
        """Access attribute by using yaml path"""
        # Walk sub_dicts before parsing path
        root = self.raw
        for sub in self.__sub_dicts:
            root = root.get(sub, None)
        # Walk each component of the path
        for comp in path.split(sep):
            if comp in root:
                root = root.get(comp)
            else:
                return default
        return root

    def y_bool(self, path: str, default=False) -> bool:
        """Wrapper for y that converts value into boolean"""
        return str(self.y(path, default)).lower() == "true"


CONFIG = ConfigLoader()
