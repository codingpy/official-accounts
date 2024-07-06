import logging

from aiohttp import web

from official_accounts.routes import setup_routes
from official_accounts.settings import get_config


async def init_app(argv=None):
    app = web.Application()

    app.update(get_config(argv))

    setup_routes(app)
    return app


async def get_app():
    """Used by aiohttp-devtools for local development."""
    import aiohttp_debugtoolbar

    app = await init_app()
    aiohttp_debugtoolbar.setup(app)
    return app


def main():
    logging.basicConfig(level=logging.DEBUG)

    app = init_app()
    web.run_app(app)


if __name__ == "__main__":
    main()
