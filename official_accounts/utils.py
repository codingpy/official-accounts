import re

import xmltodict


def to_snake(s):
    return re.sub("(?<!^)(?=[A-Z])", "_", s).lower()


def to_pascal(s):
    return re.sub("_(?=[A-Z])", "", s.title())


def parse_xml(xml):
    return xmltodict.parse(xml)["xml"]


def to_xml(d):
    return xmltodict.unparse({"xml": d}, full_document=False)
