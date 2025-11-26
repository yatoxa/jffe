import logging
import os

from aiohttp import web

from ...contrib.settings import SETTINGS_MODEL_ENV, settings
from .views import routes


def make_app(log_level: int = logging.INFO) -> web.Application:
    logging.basicConfig(level=log_level)
    app = web.Application()
    app.add_routes(routes)
    app["file_handler"] = (settings.file_handler_class)()
    return app


if __name__ == "__main__":
    os.environ.setdefault(SETTINGS_MODEL_ENV, "jffe.core.files.settings.Settings")
    web.run_app(
        make_app(),
        host=settings.web_server.http_host,
        port=settings.web_server.http_port,
        access_log_format=settings.web_server.access_log_format,
    )
