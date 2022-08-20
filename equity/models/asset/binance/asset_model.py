from marshmallow import Schema, fields


class BinanceAsset():
    def __init__(self, ticker: str, status: str, base_asset: str, quote_asset: str) -> None:
        self.ticker = ticker
        self.status = status
        self.base_asset = base_asset
        self.quote_asset = quote_asset

    def __repr__(self) -> str:
        return '<BinanceAsset(name={self.ticker!r})>'.format(self=self)


class BinanceAssetSchema(Schema):
    ticker = fields.Str()
    status = fields.Str()
    base_asset = fields.Str()
    quote_asset = fields.Str()
