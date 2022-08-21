from marshmallow import Schema, fields


class BinanceAssetData():
    def __init__(self, ticker: str, base_asset: str, quote_asset: str, price: float) -> None:
        self.ticker = ticker
        self.base_asset = base_asset
        self.quote_asset = quote_asset
        self.price = price

    def __repr__(self) -> str:
        return '<BinanceAssetData(name={self.ticker!r})>'.format(self=self)


class BinanceAssetDataSchema(Schema):
    ticker = fields.Str()
    base_asset = fields.Str()
    quote_asset = fields.Str()
    price = fields.Float()
