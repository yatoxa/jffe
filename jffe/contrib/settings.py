import os
from functools import cached_property
from typing import Any

from pydantic.v1 import BaseSettings
from pydantic.v1.utils import import_string

SETTINGS_MODEL_ENV = "JFFE_SETTINGS_MODEL"


class SettingsError(Exception):
    pass


class LoadSettingsError(SettingsError):
    pass


class BaseSettingsModel(BaseSettings):
    debug: bool = False

    @classmethod
    def load_settings(cls) -> "BaseSettingsModel":
        raise NotImplementedError


class _LazySettingsProxy:
    @cached_property
    def _settings(self) -> BaseSettings:
        settings_model_path = os.environ.get(SETTINGS_MODEL_ENV)

        try:
            return import_string(settings_model_path).load_settings()
        except Exception as e:
            raise LoadSettingsError from e

    def __getattr__(self, item: str) -> Any:
        return self.__dict__.setdefault(item, getattr(self._settings, item))


settings: BaseSettingsModel = _LazySettingsProxy()  # noqa
