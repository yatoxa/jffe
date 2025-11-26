import asyncio
from functools import cached_property
from typing import Optional, Tuple, Type

from ....contrib.settings import settings


class BaseMetaLoader:
    def __init__(self, **params) -> None:
        self._params = params

    async def save(self, *, file_id: str, meta: str) -> None:
        raise NotImplementedError

    async def load(self, file_id: str) -> Optional[str]:
        raise NotImplementedError


class BaseFileLoader:
    def __init__(self, **params) -> None:
        self._params = params

    async def save(self, file: bytes) -> str:
        raise NotImplementedError

    async def load(self, file_id: str) -> Optional[str]:
        raise NotImplementedError


class BaseFileHandler:
    file_loader_class: Type[BaseFileLoader]
    meta_loader_class: Type[BaseMetaLoader]

    @cached_property
    def file_loader(self) -> BaseFileLoader:
        return self.file_loader_class(**settings.file_loder.dict())

    @cached_property
    def meta_loader(self) -> BaseMetaLoader:
        return self.meta_loader_class(**settings.meta_loder.dict())

    async def save(self, file: bytes, meta: str) -> str:
        file_id = await self.file_loader.save(file)
        await self.meta_loader.save(file_id=file_id, meta=meta)
        return file_id

    async def load(self, file_id: str) -> Tuple[Optional[str], Optional[str]]:
        file_url, meta = await asyncio.gather(
            self.file_loader.load(file_id),
            self.meta_loader.load(file_id),
        )
        return file_url, meta
