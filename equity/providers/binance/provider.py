import requests
from requests import HTTPError
from equity.models.asset.binance.asset_data_model import BinanceAssetData

from equity.models.asset.binance.asset_model import BinanceAsset


class BinanceProvider:

    def __init__(self) -> None:
        self.BASE_URL = 'https://api.binance.com/api/v3'
        self.HEADERS = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
        }

    def __enter__(self) -> None:
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        return

    def getAvailableAssets(self, limit: int, offset: int):
        url = f'{self.BASE_URL}/exchangeInfo'
        try:
            response = requests.get(url, headers=self.HEADERS)
            response.raise_for_status()
        except HTTPError as err:
            return {'error_code': err.response.status_code, 'response': err.response.text}

        data = response.json()
        tickers = data['symbols']
        last_index = offset + limit

        value = []
        for i, asset in enumerate(tickers, start=offset):
            if i <= last_index:
                ticker = asset['symbol']
                status = asset['status']
                base_asset = asset['baseAsset']
                quote_asset = asset['quoteAsset']
                value.append(BinanceAsset(ticker=ticker, status=status,
                             base_asset=base_asset, quote_asset=quote_asset))
                continue
            break

        return value

    def getCurrentPrice(self, asset: BinanceAsset):
        url = f'{self.BASE_URL}/ticker/price?symbol={asset.ticker}'
        try:
            response = requests.get(url, headers=self.HEADERS)
            response.raise_for_status()
        except HTTPError as err:
            return {'error_code': err.response.status_code, 'response': err.response.text}

        data = response.json()

        return data

    def getAssetData(self, ticker: str):
        ticker = ticker.upper()
        url = f'{self.BASE_URL}/exchangeInfo?symbol={ticker}'
        try:
            response = requests.get(url, headers=self.HEADERS)
            response.raise_for_status()
        except HTTPError as err:
            return {'error_code': err.response.status_code, 'response': err.response.text}

        data = response.json()
        try:
            asset = data['symbols'][0]
        except KeyError:
            return {'error_code': 404, 'message': f'Asset "{ticker}" not found.'}

        status = asset['status']
        base_asset = asset['baseAsset']
        quote_asset = asset['quoteAsset']
        asset = BinanceAsset(ticker=ticker, status=status,
                             base_asset=base_asset, quote_asset=quote_asset)

        price_data = self.getCurrentPrice(asset)

        asset_data = BinanceAssetData(ticker=ticker, base_asset=asset.base_asset,
                                      quote_asset=asset.quote_asset, price=float(price_data['price']))

        return asset_data
