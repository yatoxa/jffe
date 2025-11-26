import io

from jffe.contrib.settings import SETTINGS_MODEL_ENV
from jffe.core.files.app import make_app
from jffe.core.files.file_handlers.fs import FsFileLoader

from .settings import RAW_SETTINGS_DATA_FROM_SOME_SOURCE


async def test_upload_download(aiohttp_client, monkeypatch, mocker, tmp_path):
    monkeypatch.setenv(SETTINGS_MODEL_ENV, "tests.settings.Settings")
    tmp_files_storage_dir = tmp_path / "files"
    monkeypatch.setitem(
        RAW_SETTINGS_DATA_FROM_SOME_SOURCE["file_loder"],
        "storage_dir",
        str(tmp_files_storage_dir),
    )
    tmp_meta_storage_dir = tmp_path / "meta"
    monkeypatch.setitem(
        RAW_SETTINGS_DATA_FROM_SOME_SOURCE["meta_loder"],
        "storage_dir",
        str(tmp_meta_storage_dir),
    )
    new_file_id = "some_new_uploaded_file_id"
    mocker.patch.object(FsFileLoader, "_generate_file_id", return_value=new_file_id)

    app = make_app()
    client = await aiohttp_client(app)

    dummy_file_content = b"This is some test file content."
    data = {"file_input": io.BytesIO(dummy_file_content), "meta": "SOME_META_DATA"}
    up_resp = await client.post("/upload", data=data)

    assert up_resp.status == 200
    up_resp_data = await up_resp.json()

    assert up_resp_data["status"] == "success"
    assert up_resp_data["file_id"] == new_file_id
    assert up_resp_data["size"] == len(dummy_file_content)

    assert (tmp_files_storage_dir / new_file_id).exists()
    assert (tmp_meta_storage_dir / new_file_id).exists()

    down_resp = await client.post("/download", json={"file_id": new_file_id})

    assert down_resp.status == 200
    down_resp_data = await down_resp.json()

    assert down_resp_data["status"] == "success"
    assert down_resp_data["meta"] == data["meta"]
    assert down_resp_data["file_id"] == new_file_id
    assert down_resp_data["file_url"] == app["file_handler"].file_loader._make_cdn_url(
        new_file_id
    )
