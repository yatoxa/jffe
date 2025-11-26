import os

from pydantic.v1 import BaseModel, PyObject
from yaml import full_load

from ...contrib.settings import BaseSettingsModel

CONFIG_FILE_PATH_ENV: str = "JFFE_FILES_CONFIG"


class WebServer(BaseModel):
    http_host: str = "0.0.0.0"
    http_port: int = 80

    access_log_format: str = (
        '%a %{X-Real-IP}i [%Tf] "%r" %s %b "%{Referer}i" "%{User-Agent}i"'
    )


class FileLoaderSettings(BaseModel):
    storage_dir: str = None
    cdn_base_url: str = None


class MetaLoderSettings(BaseModel):
    storage_dir: str = None


class Settings(BaseSettingsModel):
    web_server: WebServer = WebServer()

    file_loder: FileLoaderSettings = FileLoaderSettings()
    meta_loder: MetaLoderSettings = MetaLoderSettings()

    file_handler_class: PyObject = None

    @classmethod
    def load_settings(cls) -> "Settings":
        settings_file_path = os.environ.get(CONFIG_FILE_PATH_ENV)

        with open(settings_file_path) as settings_file:
            return cls(**full_load(settings_file))
