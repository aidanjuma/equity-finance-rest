import os
import pymongo
from typing import Union
from dotenv import load_dotenv
from equity.model.asset import Asset

load_dotenv()


class MongoProvider:
    def __init__(self) -> None:
        self.client = pymongo.MongoClient(os.getenv('MONGO_URI'))

    def __enter__(self) -> None:
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.client.close()

    def __parseAssets(data) -> list:
        assets = []

        for asset in data:
            asset_obj = Asset(ticker=asset['ticker'], market=asset['market'],
                              google_finance_url=asset['google_finance_url'])
            assets.append(asset_obj)

        return assets

    def getGoogleAssets(self,  limit: int, offset: int) -> list:
        collection = self.client.google.assets
        start_id = collection.find().sort('_id', pymongo.ASCENDING)
        last_id = start_id[offset]['_id']

        data = collection.find({'_id': {'$gte': last_id}}).sort(
            '_id', pymongo.ASCENDING).limit(limit)
        assets = self.__parseAssets(data)

        return assets

    def getGoogleAssetsToQuote(self, ticker: str, market: Union[str, None] = None):
        no_market = market == None

        collection = self.client.google.assets
        pipeline = [{'$match': {'ticker': ticker}}]

        # If market supplied, add to aggregate query.
        match no_market:
            case False:
                # Market supplied, add to pipeline.
                pipeline[0]['$match']['market'] = market
            case True:
                # No market supplied; retain default.
                pass

        data = collection.aggregate(pipeline=pipeline)
        assets = self.__parseAssets(data)

        return assets
