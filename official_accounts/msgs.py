import typing


class Msg:
    to_user_name: str
    from_user_name: str
    create_time: int
    msg_type: str
    msg_id: int

    def __init_subclass__(cls):
        cls.hints = typing.get_type_hints(cls)

    def __init__(self, d):
        for key, value in d.items():
            if key in self.hints:
                typ = self.hints[key]

                setattr(self, key, typ(value))


class Text(Msg):
    content: str


class Image(Msg):
    pic_url: str


class Voice(Msg):
    media_id: str
    format: str


class Video(Msg):
    media_id: str
    thumb_media_id: str


class Location(Msg):
    location_x: float
    location_y: float
    scale: int
    label: str


class Link(Msg):
    title: str
    description: str
    url: str


classes = {
    "text": Text,
    "image": Image,
    "voice": Voice,
    "video": Video,
    "location": Location,
    "link": Link,
}


def create_msg(d):
    return classes[d["msg_type"]](d)
