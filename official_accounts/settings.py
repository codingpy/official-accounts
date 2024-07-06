import argparse
import os

from dotenv import load_dotenv

load_dotenv()  # take environment variables


def get_config(argv):
    parser = argparse.ArgumentParser()

    parser.add_argument("--app-id", default=os.getenv("app_id"))
    parser.add_argument("--token", default=os.getenv("token"))
    parser.add_argument("--encoding-aes-key", default=os.getenv("encoding_aes_key"))

    args = parser.parse_args(argv)

    return vars(args)  # dict-like view of the attributes
