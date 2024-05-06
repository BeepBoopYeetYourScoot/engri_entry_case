import hashlib

from aiohttp import web
from aiohttp.web_request import Request
from aiohttp.web_routedef import RouteTableDef

hash_routes = RouteTableDef()

VALIDATION_ERROR_MESSAGE = "Missing field in the incoming JSON: '{field}'"
EMPTY_FIELD_ERROR_MESSAGE = "Got empty field: {field}"


@hash_routes.get("/healthcheck")
async def healthcheck(request: Request):
    return web.json_response(data={}, status=200)


@hash_routes.post("/hash")
async def hash(request: Request, required_field="string"):
    data = await request.json()
    if required_field not in data:
        return web.json_response(
            data={
                "validation_errors": VALIDATION_ERROR_MESSAGE.format(
                    field=required_field
                )
            },
            status=400,
        )
    string_value = data[required_field]
    if not isinstance(string_value, str):
        return web.json_response(
            data={
                "validation_errors": EMPTY_FIELD_ERROR_MESSAGE.format(
                    field=required_field
                )
            },
            status=400,
        )
    hashed_string = hashlib.sha256(string_value.encode("utf-8"))
    return web.json_response(
        data={"hash_string": hashed_string.hexdigest()}, status=200
    )
