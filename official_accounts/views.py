from aiohttp import web

from official_accounts import auth, keys


async def index(request):
    if auth.verify(
        request.query["signature"],
        request.config_dict[keys.token],
        request.query["timestamp"],
        request.query["nonce"],
    ):
        return web.Response(text=request.query["echostr"])
