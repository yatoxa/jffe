import aiohttp
import pytest

import jffe
from jffe.contrib.settings import SETTINGS_MODEL_ENV
from jffe.core.files.app import make_app


def test_get_version():
    assert jffe.get_version() == jffe.__version__.VERSION


@pytest.mark.parametrize(
    "version,expected",
    [
        pytest.param(
            None,
            "0.0.0",
            id="call-version-with-no-version",
        ),
        pytest.param(
            "some.project.version",
            "some.project.version",
            id="call-version-with-version",
        ),
    ],
)
async def test_version_call(aiohttp_client, monkeypatch, version, expected):
    monkeypatch.setenv(SETTINGS_MODEL_ENV, "tests.settings.Settings")
    client = await aiohttp_client(make_app())
    monkeypatch.setattr(jffe.__version__, "VERSION", version)
    resp = await client.get("/version")
    assert resp.status == 200
    assert await resp.text() == expected


async def test_compare_version_calls():
    async with aiohttp.ClientSession() as session:
        files_resp = await session.get("http://files/version")
        nginx_resp = await session.get("http://nginx/version")
        assert files_resp.status == 200
        assert nginx_resp.status == 200
        assert await files_resp.text() == await nginx_resp.text()
