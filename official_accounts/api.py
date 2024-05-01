base_url = "https://api.weixin.qq.com"


class Client:
    def __init__(self, session):
        self.session = session

    async def get_access_token(self, app_id, app_secret):
        return await self.get_json(
            f"/cgi-bin/token?grant_type=client_credential&appid={app_id}&secret={app_secret}"
        )

    async def get_api_domain_ip(self, access_token):
        return await self.get_json(
            f"/cgi-bin/get_api_domain_ip?access_token={access_token}"
        )

    async def get_callback_ip(self, access_token):
        return await self.get_json(
            f"/cgi-bin/getcallbackip?access_token={access_token}"
        )

    async def check_callback(
        self, access_token, action="all", check_operator="DEFAULT"
    ):
        return await self.post_json(
            f"/cgi-bin/callback/check?access_token={access_token}",
            {"action": action, "check_operator": check_operator},
        )

    async def clear_quota(self, access_token, app_id):
        return await self.post_json(
            f"/cgi-bin/clear_quota?access_token={access_token}", {"appid": app_id}
        )

    async def get_quota(self, access_token, cgi_path):
        return await self.post_json(
            f"/cgi-bin/openapi/quota/get?access_token={access_token}",
            {"cgi_path": cgi_path},
        )

    async def get_rid(self, access_token, rid):
        return await self.post_json(
            f"/cgi-bin/openapi/rid/get?access_token={access_token}", {"rid": rid}
        )

    async def clear_quota_v2(self, app_id, app_secret):
        return await self.post_json(
            f"/cgi-bin/clear_quota/v2?appid={app_id}&appsecret={app_secret}"
        )

    async def create_menu(self, access_token, button):
        return await self.post_json(
            f"/cgi-bin/menu/create?access_token={access_token}", {"button": button}
        )

    async def get_current_self_menu_info(self, access_token):
        return await self.get_json(
            f"/cgi-bin/get_current_selfmenu_info?access_token={access_token}"
        )

    async def del_menu(self, access_token):
        return await self.get_json(f"/cgi-bin/menu/delete?access_token={access_token}")

    async def add_conditional_menu(self, access_token, button, match_rule):
        return await self.post_json(
            f"/cgi-bin/menu/addconditional?access_token={access_token}",
            {"button": button, "matchrule": match_rule},
        )

    async def del_conditional_menu(self, access_token, menu_id):
        return await self.post_json(
            f"/cgi-bin/menu/delconditional?access_token={access_token}",
            {"menuid": menu_id},
        )

    async def try_match_menu(self, access_token, user_id):
        return await self.post_json(
            f"/cgi-bin/menu/trymatch?access_token={access_token}", {"user_id": user_id}
        )

    async def get_menu(self, access_token):
        return await self.get_json(f"/cgi-bin/menu/get?access_token={access_token}")

    async def get_json(self, url):
        async with self.session.get(url) as resp:
            return await resp.json()

    async def post_json(self, url, json=None):
        async with self.session.post(url, json=json) as resp:
            return await resp.json()
