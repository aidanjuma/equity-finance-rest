from marshmallow import Schema, fields


class News():
    def __init__(self, number: int, title: str, link: str, source: str, published: str, thumbnail: str) -> None:
        self.number = number
        self.title = title
        self.link = link
        self.source = source
        self.published = published
        self.thumbnail = thumbnail

    def __repr__(self) -> str:
        return '<News(name={self.title!r})>'.format(self=self)


class NewsSchema(Schema):
    number = fields.Int()
    title = fields.Str()
    link = fields.Str()
    source = fields.Str()
    published = fields.Str()
    thumbnail = fields.Str()
