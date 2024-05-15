import argparse
import logging

from aiohttp import web

from official_accounts.routes import setup_routes


async def init_app(argv=None):
    app = web.Application()

    parser = argparse.ArgumentParser()
    parser.add_argument("--token")
    args = parser.parse_args(argv)

    app["token"] = args.token

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
