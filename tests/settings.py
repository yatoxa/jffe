from jffe.core.files.settings import Settings as _BaseSettings

RAW_SETTINGS_DATA_FROM_SOME_SOURCE = {
    "file_loder": {
        "storage_dir": "/tmp/jffe/files",
        "cdn_base_url": "http://nginx/cdn",
    },
    "meta_loder": {
        "storage_dir": "/tmp/jffe/meta",
    },
    "file_handler_class": "jffe.core.files.file_handlers.fs.FsFileHandler",
}


class Settings(_BaseSettings):
    @classmethod
    def load_settings(cls) -> "Settings":
        return cls(**RAW_SETTINGS_DATA_FROM_SOME_SOURCE)
