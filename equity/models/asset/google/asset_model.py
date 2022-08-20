from marshmallow import Schema, fields


class GoogleAsset():
    def __init__(self, ticker: str, market: str, google_finance_url: str) -> None:
        self.ticker = ticker
        self.market = market
        self.google_finance_url = google_finance_url

    def __repr__(self) -> str:
        return '<GoogleAsset(name={self.ticker!r}:{self.market!r})>'.format(self=self)


class GoogleAssetSchema(Schema):
    ticker = fields.Str()
    market = fields.Str()
    google_finance_url = fields.Url()
