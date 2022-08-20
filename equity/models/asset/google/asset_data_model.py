from marshmallow import Schema, fields


class GoogleAssetData():
    def __init__(self, ticker: str, market: str, google_finance_url: str, label: str, currency: str, price: float, market_summary: dict, about: dict, news: list[dict]) -> None:
        self.ticker = ticker
        self.market = market
        self.google_finance_url = google_finance_url
        self.label = label
        self.currency = currency
        self.price = price
        self.market_summary = market_summary
        self.about = about
        self.news = news

    def __repr__(self) -> str:
        return '<AssetData(name={self.name!r})>'.format(self=self)


class GoogleAssetDataSchema(Schema):
    ticker = fields.Str()
    market = fields.Str()
    google_finance_url = fields.Url()
    label = fields.Str()
    currency = fields.Str()
    price = fields.Float()
    market_summary = fields.Dict()
    about = fields.Str()
    news = fields.List(fields.Dict())
