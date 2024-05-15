import base64
import hashlib

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad


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
    return get_random_bytes(16) + len(msg).to_bytes(4, byteorder="big") + msg + app_id


def unpack(buffer):
    msg_len = int.from_bytes(buffer[16:20], byteorder="big")
    return buffer[20 : 20 + msg_len], buffer[20 + msg_len :]
