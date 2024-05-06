import hashlib

from aiohttp import web
from aiohttp.web_request import Request
from aiohttp.web_routedef import RouteTableDef

hash_routes = RouteTableDef()

VALIDATION_ERROR_MESSAGE = "Missing field of the incoming JSON: '{field}'"
WRONG_FIELD_TYPE_ERROR_MESSAGE = (
    "Expected {expected_type} type of {field} "
    "field, got {received_type} instead"
)
HASH_ENDPOINT_REQUIRED_FIELD = "string"


@hash_routes.get("/healthcheck")
async def healthcheck(request: Request):
    """
    Check if server is working
    """
    return web.json_response(data={}, status=200)


@hash_routes.post("/hash")
async def hashing(request: Request):
    """
    SHA256 hash input string
    """
    data = await request.json()
    if HASH_ENDPOINT_REQUIRED_FIELD not in data:
        return web.json_response(
            data={
                "validation_errors": VALIDATION_ERROR_MESSAGE.format(
                    field=HASH_ENDPOINT_REQUIRED_FIELD
                )
            },
            status=400,
        )
    string_value = data[HASH_ENDPOINT_REQUIRED_FIELD]
    if not isinstance(string_value, str):
        return web.json_response(
            data={
                "validation_errors": WRONG_FIELD_TYPE_ERROR_MESSAGE.format(
                    expected_type=str,
                    field=HASH_ENDPOINT_REQUIRED_FIELD,
                    received_type=type(string_value),
                )
            },
            status=400,
        )
    hashed_string = hashlib.sha256(string_value.encode("utf-8"))
    return web.json_response(
        data={"hash_string": hashed_string.hexdigest()}, status=200
    )
