import click
from aiohttp import web

from api.router import setup_routes

app = web.Application()


@click.command()
@click.option("--host", default="0.0.0.0", help="Define server host")
@click.option("--port", default=8080, help="Define server port")
def main(host: str, port: int):
    setup_routes(app)
    web.run_app(app, host=host, port=port)


if __name__ == "__main__":
    main()
