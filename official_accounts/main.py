import argparse

from aiohttp import web

from official_accounts import keys
from official_accounts.routes import setup_routes


def init_func(argv):
    app = web.Application()
    setup_routes(app)

    parser = argparse.ArgumentParser()
    parser.add_argument("--token")
    args = parser.parse_args(argv)

    app[keys.token] = args.token

    return app
