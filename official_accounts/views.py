from aiohttp import web

from official_accounts import auth


async def index(request):
    if auth.verify(
        request.query["signature"],
        request.app["token"],
        request.query["timestamp"],
        request.query["nonce"],
    ):
        return web.Response(text=request.query["echostr"])
