from json import JSONDecodeError

from aiohttp import web

from ... import get_version

routes = web.RouteTableDef()


@routes.get("/version")
async def version(request: web.Request) -> web.Response:
    return web.Response(text=get_version() or "0.0.0")


@routes.post("/upload")
async def upload(request: web.Request) -> web.Response:
    data = await request.post()
    uploaded_file = data.get("file_input")

    if not uploaded_file or not uploaded_file.filename:
        return web.json_response(
            {
                "status": "error",
                "message": "No file uploaded or invalid file data.",
            },
            status=400,
        )

    file_handler = request.app["file_handler"]
    file_content = uploaded_file.file.read()
    file_id = await file_handler.save(file_content, data.get("meta") or "")
    return web.json_response(
        {
            "status": "success",
            "file_id": file_id,
            "size": len(file_content),
        }
    )


@routes.post("/download")
async def download(request: web.Request) -> web.Response:
    try:
        data = await request.json()
    except JSONDecodeError:
        data = {}

    file_id = data.get("file_id")

    if not file_id:
        return web.json_response(
            {
                "status": "error",
                "message": "Required parameter 'file_id' was not received.",
            },
            status=400,
        )

    file_handler = request.app["file_handler"]
    file_url, meta = await file_handler.load(file_id)

    if file_url:
        return web.json_response(
            {
                "status": "success",
                "file_url": file_url,
                "file_id": file_id,
                "meta": meta or "",
            }
        )

    return web.json_response(
        {
            "status": "error",
            "message": "File not found.",
            "file_id": file_id,
        },
        status=404,
    )
