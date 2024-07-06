from functools import wraps

from aiohttp import web
from aiohttp.abc import AbstractView

from official_accounts import auth, msgs, utils


def on_msg(f):
    @wraps(f)
    async def wrapper(*args, **kwds):
        # Supports class based views
        req = args[0]
        if isinstance(req, AbstractView):
            req = req.request

        if req.query["encrypt_type"] != "aes":
            raise web.HTTPBadRequest

        m = utils.parse_xml(await req.text())

        if not auth.verify(
            req.query["msg_signature"],
            req.app["token"],
            req.query["timestamp"],
            req.query["nonce"],
            m["encrypt"],
        ):
            raise web.HTTPBadRequest

        m = msgs.create_msg(
            utils.parse_xml(
                auth.decrypt_msg(
                    m["encrypt"], req.app["app_id"], req.app["encoding_aes_key"]
                )
            )
        )

        req["msg"] = m

        res = await f(*args, **kwds)

        # If the server cannot process and reply to the message within five seconds,
        # it can return an empty string.
        if not res:
            return web.Response(text="")

        if isinstance(res, str):
            res = {"msg_type": "text", "content": res}

        res = {
            "to_user_name": m.from_user_name,
            "from_user_name": m.to_user_name,
            "create_time": m.create_time,
            **res,
        }

        msg_encrypt = auth.encrypt_msg(
            utils.to_xml(res), req.app["app_id"], req.app["encoding_aes_key"]
        )
        msg_signature = auth.sign(
            req.app["token"], res["create_time"], req.query["nonce"], msg_encrypt
        )

        return web.Response(
            text=utils.to_xml(
                {
                    "encrypt": msg_encrypt,
                    "msg_signature": msg_signature,
                    "time_stamp": res["create_time"],
                    "nonce": req.query["nonce"],
                }
            )
        )

    return wrapper


class Handle(web.View):
    async def get(self):
        if auth.verify(
            self.request.query["signature"],
            self.request.app["token"],
            self.request.query["timestamp"],
            self.request.query["nonce"],
        ):
            return web.Response(text=self.request.query["echostr"])

    @on_msg
    async def post(self):
        return
