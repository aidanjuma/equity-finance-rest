from marshmallow import Schema, fields


class Asset():
    def __init__(self, ticker: str, market: str, google_finance_url: str) -> None:
        self.ticker = ticker
        self.market = market
        self.google_finance_url = google_finance_url

    def __repr__(self) -> str:
        return '<Asset(name={self.ticker!r}:{self.market!r})>'.format(self=self)


class AssetSchema(Schema):
    ticker = fields.Str()
    market = fields.Str()
    google_finance_url = fields.Url()
