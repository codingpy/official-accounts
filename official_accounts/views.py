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

        if not verify(req):
            raise web.HTTPBadRequest

        secure_mode = req.query.get("encrypt_type") == "aes"

        d = utils.parse_xml(await req.text())
        if secure_mode:
            if not auth.verify(
                req.query["msg_signature"],
                req.app["token"],
                req.query["timestamp"],
                req.query["nonce"],
                d["encrypt"],
            ):
                raise web.HTTPBadRequest

            d = utils.parse_xml(
                auth.decrypt_msg(
                    d["encrypt"], req.app["app_id"], req.app["encoding_aes_key"]
                )
            )

        m = msgs.create_msg(d)

        req["msg"] = m
        res = await f(*args, **kwds)

        # If the server cannot process and reply to the message within five seconds,
        # it can return an empty string.
        if res is None:
            return web.Response(text="")

        if isinstance(res, str):
            res = {"msg_type": "text", "content": res}

        res = {
            "to_user_name": m.from_user_name,
            "from_user_name": m.to_user_name,
            "create_time": m.create_time,
            **res,
        }
        msg = utils.to_xml(res)

        if secure_mode:
            msg_encrypt = auth.encrypt_msg(
                msg, req.app["app_id"], req.app["encoding_aes_key"]
            )
            msg_signature = auth.sign(
                req.app["token"], res["create_time"], req.query["nonce"], msg_encrypt
            )
            msg = utils.to_xml(
                {
                    "encrypt": msg_encrypt,
                    "msg_signature": msg_signature,
                    "time_stamp": res["create_time"],
                    "nonce": req.query["nonce"],
                }
            )

        return web.Response(text=msg)

    return wrapper


def verify(request):
    return auth.verify(
        request.query["signature"],
        request.app["token"],
        request.query["timestamp"],
        request.query["nonce"],
    )


class Handle(web.View):
    async def get(self):
        if verify(self.request):
            return web.Response(text=self.request.query["echostr"])

    @on_msg
    async def post(self):
        return
