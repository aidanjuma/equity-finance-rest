from marshmallow import Schema, fields


class AssetData():
    def __init__(self, ticker: str, market: str, google_finance_url: str, label: str, currency: str, price: float, market_cap: int, price_range: dict, about: dict, news: dict) -> None:
        self.ticker = ticker
        self.market = market
        self.google_finance_url = google_finance_url
        self.label = label
        self.currency = currency
        self.price = price
        self.market_cap = market_cap
        self.price_range = price_range
        self.about = about
        self.news = news

    def __repr__(self) -> str:
        return '<AssetData(name={self.name!r})>'.format(self=self)


class AssetDataSchema(Schema):
    ticker = fields.Str()
    market = fields.Str()
    google_finance_url = fields.Url()
    label = fields.Str()
    currency = fields.Str()
    price = fields.Float()
    market_cap = fields.Int()
    price_range = fields.Dict()
    about = fields.Dict()
    news = fields.Dict()
