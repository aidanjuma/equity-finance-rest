import os
import pymongo
from dotenv import load_dotenv
from equity.model.asset import Asset

load_dotenv()


class MongoProvider:
    def __init__(self) -> None:
        self.client = pymongo.MongoClient(os.getenv('MONGO_URI'))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.client.close()

    def getGoogleAssets(self,  limit: int, offset: int):
        collection = self.client.google.assets
        start_id = collection.find().sort('_id', pymongo.ASCENDING)
        last_id = start_id[offset]['_id']

        data = collection.find({'_id': {'$gte': last_id}}).sort(
            '_id', pymongo.ASCENDING).limit(limit)

        output = []

        for asset in data:
            asset_obj = Asset(ticker=asset['ticker'], market=asset['market'],
                              google_finance_url=asset['google_finance_url'])
            output.append(asset_obj)

        return output
