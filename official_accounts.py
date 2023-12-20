import base64
import hashlib
import re
from urllib.parse import urljoin

import requests
import xmltodict
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

base_url = "https://api.weixin.qq.com"


def get_access_token(app_id, app_secret):
    return get(
        "/cgi-bin/token",
        params={
            "grant_type": "client_credential",
            "appid": app_id,
            "secret": app_secret,
        },
    )


def get_api_domain_ip(access_token):
    return get(f"/cgi-bin/get_api_domain_ip?access_token={access_token}")


def get_callback_ip(access_token):
    return get(f"/cgi-bin/getcallbackip?access_token={access_token}")


def check_callback(access_token, action="all", check_operator="DEFAULT"):
    return post(
        f"/cgi-bin/callback/check?access_token={access_token}",
        json={"action": action, "check_operator": check_operator},
    )


def clear_quota(access_token, app_id):
    return post(
        f"/cgi-bin/clear_quota?access_token={access_token}", json={"appid": app_id}
    )


def get_quota(access_token, cgi_path):
    return post(
        f"/cgi-bin/openapi/quota/get?access_token={access_token}",
        json={"cgi_path": cgi_path},
    )


def get_rid(access_token, rid):
    return post(
        f"/cgi-bin/openapi/rid/get?access_token={access_token}", json={"rid": rid}
    )


def clear_quota_v2(app_id, app_secret):
    return post(
        "/cgi-bin/clear_quota/v2", params={"appid": app_id, "appsecret": app_secret}
    )


def create_menu(access_token, button):
    return post(
        f"/cgi-bin/menu/create?access_token={access_token}", json={"button": button}
    )


def get_current_self_menu_info(access_token):
    return get(f"/cgi-bin/get_current_selfmenu_info?access_token={access_token}")


def del_menu(access_token):
    return get(f"/cgi-bin/menu/delete?access_token={access_token}")


def add_conditional_menu(access_token, button, match_rule):
    return post(
        f"/cgi-bin/menu/addconditional?access_token={access_token}",
        json={"button": button, "matchrule": match_rule},
    )


def del_conditional_menu(access_token, menu_id):
    return post(
        f"/cgi-bin/menu/delconditional?access_token={access_token}",
        json={"menuid": menu_id},
    )


def try_match_menu(access_token, user_id):
    return post(
        f"/cgi-bin/menu/trymatch?access_token={access_token}", json={"user_id": user_id}
    )


def get_menu(access_token):
    return get(f"/cgi-bin/menu/get?access_token={access_token}")


def get(url, **kwargs):
    return request("GET", url, **kwargs)


def post(url, **kwargs):
    return request("POST", url, **kwargs)


def request(method, url, **kwargs):
    url = urljoin(base_url, url)

    r = requests.request(method, url, **kwargs)

    return r.json()


def parse(xml):
    return xmltodict.parse(xml, postprocessor=postprocessor)["xml"]


def unparse(dic):
    return xmltodict.unparse(
        {"xml": dic}, full_document=False, preprocessor=preprocessor
    )


def postprocessor(path, key, value):
    key = to_snake(key)

    if key in ["create_time", "msg_id", "scale"]:
        value = int(value)

    if key in ["location__x", "location__y"]:
        value = float(value)

    return key, value


def preprocessor(key, value):
    if key != "xml":
        key = to_camel(key)

    return key, value


def to_snake(s):
    return re.sub("(?<!^)(?=[A-Z])", "_", s).lower()


def to_camel(s):
    return re.sub("_(?=[A-Z])", "", s.title())


def verify(signature, *args):
    return signature == sign(*args)


def sign(*args):
    return sha1("".join(sorted(args)))


def sha1(s):
    return hashlib.sha1(s.encode()).hexdigest()


def encrypt(pt, encoding_aes_key):
    cipher = get_cipher(encoding_aes_key)

    return base64.b64encode(cipher.encrypt(pad(pt, 32)))


def decrypt(ct, encoding_aes_key):
    cipher = get_cipher(encoding_aes_key)

    return unpad(cipher.decrypt(base64.b64decode(ct)), 32)


def get_cipher(encoding_aes_key):
    key = base64.b64decode(encoding_aes_key + "=")

    return AES.new(key, AES.MODE_CBC, iv=key[: AES.block_size])


def pack(msg, app_id):
    msg_len = len(msg)

    return get_random_bytes(16) + msg_len.to_bytes(4, byteorder="big") + msg + app_id


def unpack(buffer):
    msg_len = int.from_bytes(buffer[16:20], byteorder="big")

    return buffer[20 : 20 + msg_len], buffer[20 + msg_len :]
