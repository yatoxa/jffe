import pathlib
from datetime import UTC, datetime
from typing import Optional

from ..utils import generate_random_string
from .base import BaseFileHandler, BaseFileLoader, BaseMetaLoader


class FsFileLoader(BaseFileLoader):
    def __init__(self, *, storage_dir: str, cdn_base_url: str, **params) -> None:
        super().__init__(**params)
        self._cdn_base_url = cdn_base_url.rstrip("/")
        self._storage_dir_path = pathlib.Path(storage_dir)
        self._storage_dir_path.mkdir(mode=0o775, parents=True, exist_ok=True)

    def _get_file_path(self, file_id: str) -> pathlib.Path:
        return self._storage_dir_path / file_id

    def _generate_file_id(self) -> str:
        random_str = generate_random_string(8)
        return datetime.now(tz=UTC).strftime("%Y%m%d%H%M%S%f") + f"_{random_str}"

    async def save(self, file: bytes) -> str:
        new_file_id = self._generate_file_id()
        new_file_path = self._get_file_path(new_file_id)

        with open(new_file_path, mode="wb") as new_file:
            new_file.write(file)

        return new_file_id

    def _make_cdn_url(self, file_id: str) -> str:
        return f"{self._cdn_base_url}/{file_id}"

    async def load(self, file_id: str) -> Optional[str]:
        if self._get_file_path(file_id).exists():
            return self._make_cdn_url(file_id)


class FsMetaLoader(BaseMetaLoader):
    def __init__(self, *, storage_dir: str, **params) -> None:
        super().__init__(**params)
        self._storage_dir_path = pathlib.Path(storage_dir)
        self._storage_dir_path.mkdir(mode=0o775, parents=True, exist_ok=True)

    async def save(self, *, file_id: str, meta: str) -> None:
        new_meta_file_name = self._storage_dir_path / file_id

        with open(new_meta_file_name, mode="w") as new_meta_file:
            new_meta_file.write(meta)

    async def load(self, file_id: str) -> Optional[str]:
        meta_file_name = self._storage_dir_path / file_id

        if not meta_file_name.exists():
            return None

        with open(meta_file_name, mode="r") as meta_file:
            meta = meta_file.read()

        return meta


class FsFileHandler(BaseFileHandler):
    file_loader_class = FsFileLoader
    meta_loader_class = FsMetaLoader
