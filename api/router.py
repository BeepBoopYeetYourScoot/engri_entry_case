from aiohttp import web

from api.endpoints import hash_routes


def setup_routes(app: web.Application):
    app.router.add_routes(hash_routes)
