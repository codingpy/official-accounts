import re

import xmltodict


def parse_xml(xml):
    def postprocessor(path, key, value):
        key = to_snake(key)

        return key, value

    return xmltodict.parse(xml, postprocessor=postprocessor)["xml"]


def to_xml(d):
    def preprocessor(key, value):
        if key != "xml":
            key = to_pascal(key)

        return key, value

    return xmltodict.unparse({"xml": d}, full_document=False, preprocessor=preprocessor)


def to_snake(s):
    return re.sub("(?<=[^_])((?=[A-Z][a-z])|(?<=[^A-Z])(?=[A-Z]))", "_", s).lower()


def to_pascal(s):
    return re.sub("_(?=[A-Z])", "", s.title())
